package com.backend.auth;

import lombok.Data;

@Data
public class tokenResponse {

    private String token;
    private String refreshToken;
}
