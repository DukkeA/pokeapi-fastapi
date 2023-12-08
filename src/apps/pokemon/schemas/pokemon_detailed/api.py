from typing import Any, List

from pydantic import BaseModel, Field


class PokemonAbility1(BaseModel):
    name: str
    url: str


class PokemonAbility(BaseModel):
    ability: PokemonAbility1
    is_hidden: bool
    slot: int


class DreamWorld(BaseModel):
    front_default: str
    front_female: Any


class Home(BaseModel):
    front_default: str
    front_female: Any
    front_shiny: str
    front_shiny_female: Any


class OfficialArtwork(BaseModel):
    front_default: str
    front_shiny: str


class Other(BaseModel):
    dream_world: DreamWorld
    home: Home
    official_artwork: OfficialArtwork = Field(..., alias="official-artwork")


class RedBlue(BaseModel):
    back_default: str
    back_gray: str
    back_transparent: str
    front_default: str
    front_gray: str
    front_transparent: str


class Yellow(BaseModel):
    back_default: str
    back_gray: str
    back_transparent: str
    front_default: str
    front_gray: str
    front_transparent: str


class GenerationI(BaseModel):
    red_blue: RedBlue = Field(..., alias="red-blue")
    yellow: Yellow


class Crystal(BaseModel):
    back_default: str
    back_shiny: str
    back_shiny_transparent: str
    back_transparent: str
    front_default: str
    front_shiny: str
    front_shiny_transparent: str
    front_transparent: str


class Gold(BaseModel):
    back_default: str
    back_shiny: str
    front_default: str
    front_shiny: str
    front_transparent: str


class Silver(BaseModel):
    back_default: str
    back_shiny: str
    front_default: str
    front_shiny: str
    front_transparent: str


class GenerationIi(BaseModel):
    crystal: Crystal
    gold: Gold
    silver: Silver


class Emerald(BaseModel):
    front_default: str
    front_shiny: str


class FireredLeafgreen(BaseModel):
    back_default: str
    back_shiny: str
    front_default: str
    front_shiny: str


class RubySapphire(BaseModel):
    back_default: str
    back_shiny: str
    front_default: str
    front_shiny: str


class GenerationIii(BaseModel):
    emerald: Emerald
    firered_leafgreen: FireredLeafgreen = Field(..., alias="firered-leafgreen")
    ruby_sapphire: RubySapphire = Field(..., alias="ruby-sapphire")


class DiamondPearl(BaseModel):
    back_default: str
    back_female: Any
    back_shiny: str
    back_shiny_female: Any
    front_default: str
    front_female: Any
    front_shiny: str
    front_shiny_female: Any


class HeartgoldSoulsilver(BaseModel):
    back_default: str
    back_female: Any
    back_shiny: str
    back_shiny_female: Any
    front_default: str
    front_female: Any
    front_shiny: str
    front_shiny_female: Any


class Platinum(BaseModel):
    back_default: str
    back_female: Any
    back_shiny: str
    back_shiny_female: Any
    front_default: str
    front_female: Any
    front_shiny: str
    front_shiny_female: Any


class GenerationIv(BaseModel):
    diamond_pearl: DiamondPearl = Field(..., alias="diamond-pearl")
    heartgold_soulsilver: HeartgoldSoulsilver = Field(
        ..., alias="heartgold-soulsilver"
    )
    platinum: Platinum


class Animated(BaseModel):
    back_default: str
    back_female: Any
    back_shiny: str
    back_shiny_female: Any
    front_default: str
    front_female: Any
    front_shiny: str
    front_shiny_female: Any


class BlackWhite(BaseModel):
    animated: Animated
    back_default: str
    back_female: Any
    back_shiny: str
    back_shiny_female: Any
    front_default: str
    front_female: Any
    front_shiny: str
    front_shiny_female: Any


class GenerationV(BaseModel):
    black_white: BlackWhite = Field(..., alias="black-white")


class OmegarubyAlphasapphire(BaseModel):
    front_default: str
    front_female: Any
    front_shiny: str
    front_shiny_female: Any


class XY(BaseModel):
    front_default: str
    front_female: Any
    front_shiny: str
    front_shiny_female: Any


class GenerationVi(BaseModel):
    omegaruby_alphasapphire: OmegarubyAlphasapphire = Field(
        ..., alias="omegaruby-alphasapphire"
    )
    x_y: XY = Field(..., alias="x-y")


class Icons(BaseModel):
    front_default: str
    front_female: Any


class UltraSunUltraMoon(BaseModel):
    front_default: str
    front_female: Any
    front_shiny: str
    front_shiny_female: Any


class GenerationVii(BaseModel):
    icons: Icons
    ultra_sun_ultra_moon: UltraSunUltraMoon = Field(
        ..., alias="ultra-sun-ultra-moon"
    )


class Icons1(BaseModel):
    front_default: str
    front_female: Any


class GenerationViii(BaseModel):
    icons: Icons1


class PokemonSpriteVersion(BaseModel):
    generation_i: GenerationI = Field(..., alias="generation-i")
    generation_ii: GenerationIi = Field(..., alias="generation-ii")
    generation_iii: GenerationIii = Field(..., alias="generation-iii")
    generation_iv: GenerationIv = Field(..., alias="generation-iv")
    generation_v: GenerationV = Field(..., alias="generation-v")
    generation_vi: GenerationVi = Field(..., alias="generation-vi")
    generation_vii: GenerationVii = Field(..., alias="generation-vii")
    generation_viii: GenerationViii = Field(..., alias="generation-viii")


class PokemonSprite(BaseModel):
    back_default: str
    back_female: Any
    back_shiny: str
    back_shiny_female: Any
    front_default: str
    front_female: Any
    front_shiny: str
    front_shiny_female: Any
    other: Other
    versions: PokemonSpriteVersion


class PokemonType1(BaseModel):
    name: str
    url: str


class PokemonType(BaseModel):
    slot: int
    type: PokemonType1


class Pokemon(BaseModel):
    abilities: List[PokemonAbility]
    id: int
    name: str
    sprites: PokemonSprite
    types: List[PokemonType]
