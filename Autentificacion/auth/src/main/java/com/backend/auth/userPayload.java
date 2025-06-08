package com.backend.auth;

import lombok.Data;

@Data
public class userPayload {
    private String id;
    private String username;
    private String role;

}
