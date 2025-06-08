package com.backend.auth;


import io.jsonwebtoken.*;
import io.jsonwebtoken.security.Keys;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;

import javax.crypto.SecretKey;
import java.util.Date;
import java.util.HashMap;
import java.util.Map;
import java.util.Objects;

@Service
public class authService {

    @Value("${app.JWT_SECRET_KEY}")
    private String jwtSecret;
    @Value("${app.REFRESH_TOKEN_SECRET_KEY}")
    private String refreshTokenSecret;

    private SecretKey getSigningKey() {
        return Keys.hmacShaKeyFor(jwtSecret.getBytes());
    }

    private SecretKey getRefreshSigningKey() {
        return Keys.hmacShaKeyFor(refreshTokenSecret.getBytes());
    }
    public String generateAccessToken(userPayload payload) {
        Map<String, Object> claims = new HashMap<>();
        claims.put("id", payload.getId());
        claims.put("username", payload.getUsername()); // Ensure this is set correctly
        claims.put("role", payload.getRole());
        Long time = 1 * 60 * 60 * 1000L; // 1 hour in milliseconds
        return Jwts.builder()
                .setClaims(claims)
                .setSubject(payload.getId())
                .setIssuedAt(new Date(System.currentTimeMillis()))
                .setExpiration(new Date(System.currentTimeMillis() + time))
                .signWith(getSigningKey(), SignatureAlgorithm.HS256)
                .compact();
    }

    public String generateRefreshToken(userPayload payload){
        // calcular 1 dia
        Long time = 24 * 60 * 60 * 1000L;
        return Jwts.builder()
                .setSubject(payload.getId())
                .claim("email", payload.getUsername())
                .claim("role", payload.getRole())
                .claim("username", payload.getUsername())
                .setIssuedAt(new Date(System.currentTimeMillis()))
                .setExpiration(new Date(System.currentTimeMillis() + time))
                .signWith(getRefreshSigningKey(), SignatureAlgorithm.HS256)
                .compact();
    }

    public Claims extractClaims(String token) {
        return Jwts.parserBuilder()
                .setSigningKey(getSigningKey())
                .build()
                .parseClaimsJws(token)
                .getBody();
    }

    public Claims extractRefreshClaims(String refreshToken) {
        return Jwts.parserBuilder()
                .setSigningKey(getRefreshSigningKey())
                .build()
                .parseClaimsJws(refreshToken)
                .getBody();
    }

    public boolean isTokenValid(String token) {
        try {
            if (token == null || token.isBlank()) {
                return false;
            }
            Claims claims = extractClaims(token);

            return claims.getExpiration().after(new Date());
        } catch (JwtException | IllegalArgumentException e) {
            return false;
        }
    }

    public boolean isRefreshTokenValid(String refreshToken) {
        if (refreshToken == null || refreshToken.isBlank()) {
            return false;
        }

        try {
            Claims claims = extractRefreshClaims(refreshToken);
            return claims.getExpiration().after(new Date());
        } catch (ExpiredJwtException ex) {
            return false;
        } catch (JwtException | IllegalArgumentException ex) {
            return false;
        }
    }

    public userPayload extractUserFromToken(String token) {
        Claims claims = extractClaims(token);
        userPayload user = new userPayload();
        user.setId(claims.getSubject());
        user.setUsername(claims.get("username", String.class));
        System.out.println(claims.get("username", String.class));
        user.setRole(claims.get("role", String.class));
        return user;
    }

    public userPayload extractUserFromRefreshToken(String refreshToken) {
        Claims claims = extractRefreshClaims(refreshToken);
        userPayload user = new userPayload();
        user.setId(claims.getSubject());
        user.setUsername(claims.get("username", String.class));
        user.setRole(claims.get("role", String.class));
        return user;
    }

    public boolean hasRole(String token, String requiredRole) {
        try {
            Claims claims = extractClaims(token);
            String userRole = claims.get("role", String.class);
            return requiredRole.equalsIgnoreCase(userRole);
        } catch (JwtException | IllegalArgumentException e) {
            return false;
        }
    }

    public String getUsernameFromToken(String token) {
        try {
            Claims claims = extractClaims(token);
            return claims.get("username", String.class);
        } catch (JwtException | IllegalArgumentException e) {
            throw new RuntimeException("Invalid token while extracting username", e);
        }
    }

    public tokenResponse refreshTokenPair(String refreshToken) {
        if (!isRefreshTokenValid(refreshToken)) {
            throw new RuntimeException("Invalid refresh token");
        }

        userPayload user = extractUserFromRefreshToken(refreshToken);
        String newAccessToken = generateAccessToken(user);
        String newRefreshToken = generateRefreshToken(user);

        tokenResponse response = new tokenResponse();
        response.setToken(newAccessToken);
        response.setRefreshToken(newRefreshToken);
        return response;
    }
}