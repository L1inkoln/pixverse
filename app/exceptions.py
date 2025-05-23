from fastapi import HTTPException, status

PIXVERSE_ERROR_MAP = {
    400011: (status.HTTP_422_UNPROCESSABLE_ENTITY, "Empty parameter"),
    400012: (status.HTTP_401_UNAUTHORIZED, "Invalid account"),
    400013: (status.HTTP_400_BAD_REQUEST, "Invalid binding request"),
    400017: (status.HTTP_422_UNPROCESSABLE_ENTITY, "Invalid parameter"),
    400018: (status.HTTP_413_REQUEST_ENTITY_TOO_LARGE, "Prompt too long"),
    400019: (status.HTTP_413_REQUEST_ENTITY_TOO_LARGE, "Prompt too long"),
    400032: (status.HTTP_422_UNPROCESSABLE_ENTITY, "Invalid image ID"),
    500008: (status.HTTP_404_NOT_FOUND, "Requested data not found"),
    500020: (status.HTTP_403_FORBIDDEN, "Permission denied"),
    500030: (status.HTTP_413_REQUEST_ENTITY_TOO_LARGE, "Image too large"),
    500031: (status.HTTP_422_UNPROCESSABLE_ENTITY, "Image info retrieval failed"),
    500032: (status.HTTP_415_UNSUPPORTED_MEDIA_TYPE, "Invalid image format"),
    500033: (status.HTTP_422_UNPROCESSABLE_ENTITY, "Invalid image size"),
    500041: (status.HTTP_500_INTERNAL_SERVER_ERROR, "Image upload failed"),
    500042: (status.HTTP_422_UNPROCESSABLE_ENTITY, "Invalid image path"),
    500043: (status.HTTP_402_PAYMENT_REQUIRED, "All credits used. Upgrade or top up."),
    500044: (status.HTTP_429_TOO_MANY_REQUESTS, "Concurrent limit reached"),
    500054: (status.HTTP_403_FORBIDDEN, "Content moderation failure"),
    500060: (status.HTTP_429_TOO_MANY_REQUESTS, "Monthly limit reached"),
    500063: (status.HTTP_403_FORBIDDEN, "Prompt blocked by AI moderator"),
    500064: (status.HTTP_404_NOT_FOUND, "Content deleted"),
    500069: (status.HTTP_503_SERVICE_UNAVAILABLE, "System overloaded"),
    500070: (status.HTTP_400_BAD_REQUEST, "Template not activated"),
    500071: (status.HTTP_400_BAD_REQUEST, "Effect doesn't support resolution"),
    500090: (status.HTTP_402_PAYMENT_REQUIRED, "Insufficient balance"),
    500100: (status.HTTP_500_INTERNAL_SERVER_ERROR, "Internal database error"),
    99999: (status.HTTP_500_INTERNAL_SERVER_ERROR, "Unknown error"),
}


def raise_for_pixverse_error(err_code: int, err_msg: str = ""):
    http_status, default_msg = PIXVERSE_ERROR_MAP.get(
        err_code, (status.HTTP_500_INTERNAL_SERVER_ERROR, "Unhandled Pixverse error")
    )
    raise HTTPException(status_code=http_status, detail=err_msg or default_msg)
