from . import Data


class DataHeader(Data):
    result_code: int
    viewer_id: int
    sid: str
    servertime: int
    buma_session_token: str
    notifications: dict


class ResponseCommon(Data):
    data_headers: DataHeader
    response_code: int
