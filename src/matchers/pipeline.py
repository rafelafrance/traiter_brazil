"""Create a trait pipeline."""

# pylint: disable=import-error

from traiter.matchers.rule import Rule
from traiter.matchers.term import Term
from traiter.pipeline import SpacyPipeline
from traiter.sentencizer import Sentencizer
from traiter.to_entities import ToEntities

from .attach import attach
from .count import COUNT
from .inflorescence import INFLORESCENCE
from .margin import MARGIN
from .morphism import MORPHISM
from .part import PART
from .shape import SHAPE
from .size import SIZE
from .surface import SURFACE
from ..pylib.consts import ABBREVS, GROUP_STEP, LINK_STEP, TERMS, TRAIT_STEP

MATCHERS = [
    COUNT, INFLORESCENCE, MARGIN, MORPHISM, PART, SHAPE, SIZE, SURFACE]


class Pipeline(SpacyPipeline):  # pylint: disable=too-few-public-methods
    """Build a custom traiter pipeline."""

    def __init__(self) -> None:
        super().__init__()

        self.nlp.disable_pipes(['ner'])

        token2entity = {TRAIT_STEP, LINK_STEP, GROUP_STEP}

        Term.add_pipes(self.nlp, TERMS, before='parser')
        Rule.add_pipe(self.nlp, MATCHERS, GROUP_STEP, before='parser')
        Rule.add_pipe(self.nlp, MATCHERS, TRAIT_STEP, before='parser')
        ToEntities.add_pipe(self.nlp, token2entity=token2entity, before='parser')
        Sentencizer.add_pipe(self.nlp, ABBREVS, before='parser')
        self.nlp.add_pipe(attach, last=True, name=LINK_STEP)
