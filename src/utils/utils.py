import logging
import warnings
from typing import List, Sequence

import pytorch_lightning as pl
import rich.syntax
import rich.tree
from jammy import link_hyd_run
from omegaconf import DictConfig, OmegaConf
from pytorch_lightning.utilities import rank_zero_only


def get_logger(name=__name__) -> logging.Logger:
    """Initializes multi-GPU-friendly python logger."""

    _logger = logging.getLogger(name)

    # this ensures all logging levels get marked with the rank zero decorator
    # otherwise logs would get multiplied for each GPU process in multi-GPU setup
    for level in (
        "debug",
        "info",
        "warning",
        "error",
        "exception",
        "fatal",
        "critical",
    ):
        setattr(_logger, level, rank_zero_only(getattr(_logger, level)))

    return _logger


g_logger = get_logger(__name__)


def extras(config: DictConfig) -> None:
    """A couple of optional utilities, controlled by main config file:
    - disabling warnings
    - forcing debug friendly configuration
    - verifying experiment name is set when running in experiment mode

    Modifies DictConfig in place.

    Args:
        config (DictConfig): Configuration composed by Hydra.
    """

    log = get_logger(__name__)

    # quick link
    rank_zero_only(link_hyd_run)()
    # disable python warnings if <config.ignore_warnings=True>
    if config.get("ignore_warnings"):
        log.info("Disabling python warnings! <config.ignore_warnings=True>")
        warnings.filterwarnings("ignore")

    # verify experiment name is set when running in experiment mode
    if config.get("experiment_mode") and not config.get("name"):
        log.info(
            "Running in experiment mode without the experiment name specified! "
            "Use `python run.py mode=exp name=experiment_name`"
        )
        log.info("Exiting...")
        exit()

    # force debugger friendly configuration if <config.trainer.fast_dev_run=True>
    # debuggers don't like GPUs and multiprocessing
    if config.trainer.get("fast_dev_run"):
        log.info(
            "Forcing debugger friendly configuration! <config.trainer.fast_dev_run=True>"
        )
        if config.trainer.get("gpus"):
            config.trainer.gpus = 0
        if config.datamodule.get("pin_memory"):
            config.datamodule.pin_memory = False
        if config.datamodule.get("num_workers"):
            config.datamodule.num_workers = 0


@rank_zero_only
def print_config(
    config: DictConfig,
    fields: Sequence[str] = (
        "trainer",
        "model",
        "datamodule",
        "callbacks",
        "logger",
        "test_after_training",
        "seed",
        "name",
    ),
    resolve: bool = True,
) -> None:
    """Prints content of DictConfig using Rich library and its tree structure.

    Args:
        config (DictConfig): Configuration composed by Hydra.
        fields (Sequence[str], optional): Determines which main fields from config will
        be printed and in what order.
        resolve (bool, optional): Whether to resolve reference fields of DictConfig.
    """

    style = "dim"
    tree = rich.tree.Tree("CONFIG", style=style, guide_style=style)

    for field in fields:
        branch = tree.add(field, style=style, guide_style=style)

        config_section = config.get(field)
        branch_content = str(config_section)
        if isinstance(config_section, DictConfig):
            branch_content = OmegaConf.to_yaml(config_section, resolve=resolve)

        branch.add(rich.syntax.Syntax(branch_content, "yaml"))

    rich.print(tree)

    with open("config_tree.txt", "w", encoding="utf-8") as fp:
        rich.print(tree, file=fp)


def empty(*args, **kwargs):  # pylint: disable=unused-argument
    pass


@rank_zero_only
def log_hyperparameters(
    config: DictConfig,
    model: pl.LightningModule,
    datamodule: pl.LightningDataModule,
    trainer: pl.Trainer,
    callbacks: List[pl.Callback],
    logger: List[pl.loggers.LightningLoggerBase],
) -> None:
    """This method controls which parameters from Hydra config are saved by Lightning loggers.

    Additionaly saves:
        - number of trainable model parameters
    """
    del datamodule, callbacks, logger

    hparams = {}

    # choose which parts of hydra config will be saved to loggers
    hparams["trainer"] = config["trainer"]
    hparams["model"] = config["model"]
    hparams["datamodule"] = config["datamodule"]
    if "seed" in config:
        hparams["seed"] = config["seed"]
    if "callbacks" in config:
        hparams["callbacks"] = config["callbacks"]

    # save number of model parameters
    hparams["model/params_total"] = sum(p.numel() for p in model.parameters())
    hparams["model/params_trainable"] = sum(
        p.numel() for p in model.parameters() if p.requires_grad
    )
    hparams["model/params_not_trainable"] = sum(
        p.numel() for p in model.parameters() if not p.requires_grad
    )

    # send hparams to all loggers
    trainer.logger.log_hyperparams(hparams)

    # disable logging any more hyperparameters for all loggers
    # this is just a trick to prevent trainer from logging hparams of model,
    # since we already did that above
    trainer.logger.log_hyperparams = empty


def auto_fgpu(config: DictConfig):
    # FIXME: only support one gpu, quick select
    if config.fgpu:
        if getattr(config.trainer, "gpus", 0) == 1:
            from jammy.utils.gpu import select_gpu

            best_id = select_gpu(mem_prior=0.1)
            config.trainer.gpus = [
                best_id,
            ]
            g_logger.warning(f"fgpu select device {best_id}")
        elif int(getattr(config.trainer, "gpus", 0)) > 1:
            g_logger.warning(f"fgpu only support gpus=1, but get {config.trainer.gpus}")


def finish(  # pylint: disable= unused-argument
    config: DictConfig,
    model: pl.LightningModule,
    datamodule: pl.LightningDataModule,
    trainer: pl.Trainer,
    callbacks: List[pl.Callback],
    logger: List[pl.loggers.LightningLoggerBase],
) -> None:
    """Makes sure everything closed properly."""

    # without this sweeps with wandb logger might crash!
    for clogger in logger:
        from src.logger.wandb_logger import WandbLogger

        if isinstance(clogger, WandbLogger):
            from src.logger.jam_wandb import JamWandb

            JamWandb.finish()
