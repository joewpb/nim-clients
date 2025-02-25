from google.protobuf import empty_pb2 as _empty_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ModelSelection(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    MODEL_SELECTION_UNSPECIFIED: _ClassVar[ModelSelection]
    MODEL_SELECTION_PERF: _ClassVar[ModelSelection]
    MODEL_SELECTION_QUALITY: _ClassVar[ModelSelection]

class AnimationCroppingMode(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    ANIMATION_CROPPING_MODE_UNSPECIFIED: _ClassVar[AnimationCroppingMode]
    ANIMATION_CROPPING_MODE_FACEBOX: _ClassVar[AnimationCroppingMode]
    ANIMATION_CROPPING_MODE_REGISTRATION_BLENDING: _ClassVar[AnimationCroppingMode]
    ANIMATION_CROPPING_MODE_INSET_BLENDING: _ClassVar[AnimationCroppingMode]

class HeadPoseMode(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    HEAD_POSE_MODE_UNSPECIFIED: _ClassVar[HeadPoseMode]
    HEAD_POSE_MODE_RETAIN_FROM_PORTRAIT_IMAGE: _ClassVar[HeadPoseMode]
    HEAD_POSE_MODE_PRE_DEFINED_ANIMATION: _ClassVar[HeadPoseMode]
    HEAD_POSE_MODE_USER_DEFINED_ANIMATION: _ClassVar[HeadPoseMode]
MODEL_SELECTION_UNSPECIFIED: ModelSelection
MODEL_SELECTION_PERF: ModelSelection
MODEL_SELECTION_QUALITY: ModelSelection
ANIMATION_CROPPING_MODE_UNSPECIFIED: AnimationCroppingMode
ANIMATION_CROPPING_MODE_FACEBOX: AnimationCroppingMode
ANIMATION_CROPPING_MODE_REGISTRATION_BLENDING: AnimationCroppingMode
ANIMATION_CROPPING_MODE_INSET_BLENDING: AnimationCroppingMode
HEAD_POSE_MODE_UNSPECIFIED: HeadPoseMode
HEAD_POSE_MODE_RETAIN_FROM_PORTRAIT_IMAGE: HeadPoseMode
HEAD_POSE_MODE_PRE_DEFINED_ANIMATION: HeadPoseMode
HEAD_POSE_MODE_USER_DEFINED_ANIMATION: HeadPoseMode

class AnimateConfig(_message.Message):
    __slots__ = ("portrait_image", "model_selection", "animation_crop_mode", "head_pose_mode", "enable_lookaway", "lookaway_max_offset", "lookaway_interval_range", "lookaway_interval_min", "blink_frequency", "blink_duration", "mouth_expression_multiplier", "head_pose_multiplier", "input_head_rotation", "input_head_translation")
    PORTRAIT_IMAGE_FIELD_NUMBER: _ClassVar[int]
    MODEL_SELECTION_FIELD_NUMBER: _ClassVar[int]
    ANIMATION_CROP_MODE_FIELD_NUMBER: _ClassVar[int]
    HEAD_POSE_MODE_FIELD_NUMBER: _ClassVar[int]
    ENABLE_LOOKAWAY_FIELD_NUMBER: _ClassVar[int]
    LOOKAWAY_MAX_OFFSET_FIELD_NUMBER: _ClassVar[int]
    LOOKAWAY_INTERVAL_RANGE_FIELD_NUMBER: _ClassVar[int]
    LOOKAWAY_INTERVAL_MIN_FIELD_NUMBER: _ClassVar[int]
    BLINK_FREQUENCY_FIELD_NUMBER: _ClassVar[int]
    BLINK_DURATION_FIELD_NUMBER: _ClassVar[int]
    MOUTH_EXPRESSION_MULTIPLIER_FIELD_NUMBER: _ClassVar[int]
    HEAD_POSE_MULTIPLIER_FIELD_NUMBER: _ClassVar[int]
    INPUT_HEAD_ROTATION_FIELD_NUMBER: _ClassVar[int]
    INPUT_HEAD_TRANSLATION_FIELD_NUMBER: _ClassVar[int]
    portrait_image: bytes
    model_selection: ModelSelection
    animation_crop_mode: AnimationCroppingMode
    head_pose_mode: HeadPoseMode
    enable_lookaway: bool
    lookaway_max_offset: int
    lookaway_interval_range: int
    lookaway_interval_min: int
    blink_frequency: int
    blink_duration: int
    mouth_expression_multiplier: float
    head_pose_multiplier: float
    input_head_rotation: QuaternionStream
    input_head_translation: Vector3fStream
    def __init__(self, portrait_image: _Optional[bytes] = ..., model_selection: _Optional[_Union[ModelSelection, str]] = ..., animation_crop_mode: _Optional[_Union[AnimationCroppingMode, str]] = ..., head_pose_mode: _Optional[_Union[HeadPoseMode, str]] = ..., enable_lookaway: bool = ..., lookaway_max_offset: _Optional[int] = ..., lookaway_interval_range: _Optional[int] = ..., lookaway_interval_min: _Optional[int] = ..., blink_frequency: _Optional[int] = ..., blink_duration: _Optional[int] = ..., mouth_expression_multiplier: _Optional[float] = ..., head_pose_multiplier: _Optional[float] = ..., input_head_rotation: _Optional[_Union[QuaternionStream, _Mapping]] = ..., input_head_translation: _Optional[_Union[Vector3fStream, _Mapping]] = ...) -> None: ...

class Vector3f(_message.Message):
    __slots__ = ("x", "y", "z")
    X_FIELD_NUMBER: _ClassVar[int]
    Y_FIELD_NUMBER: _ClassVar[int]
    Z_FIELD_NUMBER: _ClassVar[int]
    x: float
    y: float
    z: float
    def __init__(self, x: _Optional[float] = ..., y: _Optional[float] = ..., z: _Optional[float] = ...) -> None: ...

class Vector3fStream(_message.Message):
    __slots__ = ("values",)
    VALUES_FIELD_NUMBER: _ClassVar[int]
    values: _containers.RepeatedCompositeFieldContainer[Vector3f]
    def __init__(self, values: _Optional[_Iterable[_Union[Vector3f, _Mapping]]] = ...) -> None: ...

class Quaternion(_message.Message):
    __slots__ = ("x", "y", "z", "w")
    X_FIELD_NUMBER: _ClassVar[int]
    Y_FIELD_NUMBER: _ClassVar[int]
    Z_FIELD_NUMBER: _ClassVar[int]
    W_FIELD_NUMBER: _ClassVar[int]
    x: float
    y: float
    z: float
    w: float
    def __init__(self, x: _Optional[float] = ..., y: _Optional[float] = ..., z: _Optional[float] = ..., w: _Optional[float] = ...) -> None: ...

class QuaternionStream(_message.Message):
    __slots__ = ("values",)
    VALUES_FIELD_NUMBER: _ClassVar[int]
    values: _containers.RepeatedCompositeFieldContainer[Quaternion]
    def __init__(self, values: _Optional[_Iterable[_Union[Quaternion, _Mapping]]] = ...) -> None: ...

class AnimateRequest(_message.Message):
    __slots__ = ("config", "audio_file_data")
    CONFIG_FIELD_NUMBER: _ClassVar[int]
    AUDIO_FILE_DATA_FIELD_NUMBER: _ClassVar[int]
    config: AnimateConfig
    audio_file_data: bytes
    def __init__(self, config: _Optional[_Union[AnimateConfig, _Mapping]] = ..., audio_file_data: _Optional[bytes] = ...) -> None: ...

class AnimateResponse(_message.Message):
    __slots__ = ("config", "video_file_data", "keep_alive")
    CONFIG_FIELD_NUMBER: _ClassVar[int]
    VIDEO_FILE_DATA_FIELD_NUMBER: _ClassVar[int]
    KEEP_ALIVE_FIELD_NUMBER: _ClassVar[int]
    config: AnimateConfig
    video_file_data: bytes
    keep_alive: _empty_pb2.Empty
    def __init__(self, config: _Optional[_Union[AnimateConfig, _Mapping]] = ..., video_file_data: _Optional[bytes] = ..., keep_alive: _Optional[_Union[_empty_pb2.Empty, _Mapping]] = ...) -> None: ...
