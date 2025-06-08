package com.backend.auth;


import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api/auth")
public class AuthController {
    @Autowired
    private authService auth;
    
    @PostMapping("/generate-token")
    public ResponseEntity<?> generateToken(@RequestBody tokenRequest tokenRequest) {
        try{
            userPayload payload = new userPayload();
            payload.setId(tokenRequest.getId());
            payload.setUsername(tokenRequest.getUsername());
            payload.setRole(tokenRequest.getRole());

            String accessToken = auth.generateAccessToken(payload);
            String refreshToken = auth.generateRefreshToken(payload);
            tokenResponse response = new tokenResponse();
            response.setToken(accessToken);
            response.setRefreshToken(refreshToken);
            return  ResponseEntity.ok(response);
        }catch (Exception e){
            return ResponseEntity.badRequest().body("Error generating token: " + e.getMessage());
        }
    }
    @PostMapping("/refresh")
    public ResponseEntity<?> refreshToken(@RequestBody refreshTokenRequest request) {
        try {
            if (!auth.isRefreshTokenValid(request.getRefreshToken())) {
                return ResponseEntity.badRequest().build();
            }

            userPayload payload = auth.extractUserFromRefreshToken(request.getRefreshToken());

            String newAccessToken = auth.generateAccessToken(payload);

            tokenResponse response = new tokenResponse();
            response.setToken(newAccessToken);
            response.setRefreshToken(request.getRefreshToken());
            return ResponseEntity.ok(response);
        } catch (Exception e) {
            return ResponseEntity.badRequest().build();
        }
    }

    @GetMapping("/validate")
    public ResponseEntity<userPayload> validateToken(@RequestHeader("Authorization") String token) {
        try {
            token = token.replace("Bearer ", "").trim();

            if (auth.isTokenValid(token)) {
                userPayload payload = auth.extractUserFromToken(token);
                return ResponseEntity.ok(payload);
            } else {
                return ResponseEntity.badRequest().build();
            }
        } catch (Exception e) {
            return ResponseEntity.badRequest().build();
        }
    }


}
