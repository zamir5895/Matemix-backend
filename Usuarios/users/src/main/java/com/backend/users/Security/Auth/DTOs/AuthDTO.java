package com.backend.users.Security.Auth.DTOs;


import lombok.Data;

@Data
public class AuthDTO {
    private String username;
    private String id;
    private String role;
}
