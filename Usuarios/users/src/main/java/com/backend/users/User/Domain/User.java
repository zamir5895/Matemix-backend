package com.backend.users.User.Domain;

import jakarta.persistence.*;

import java.time.ZonedDateTime;
import java.util.Collection;
import java.util.List;

import lombok.Data;
import org.springframework.security.core.GrantedAuthority;
import org.springframework.security.core.authority.SimpleGrantedAuthority;
import org.springframework.security.core.userdetails.UserDetails;

@Table(name="users")
@Entity
@Inheritance(strategy = InheritanceType.JOINED)
@Data
public class User  {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    @Column(name = "role", nullable = false)
    private Rol role;

    @Column(name = "first_name", nullable = false)
    private String firstName;

    @Column(name = "last_name", nullable = false)
    private String lastName;

    @Column(name= "password", nullable = false)
    private String password;

    @Column(name = "created_at", nullable = false)
    private ZonedDateTime createdAt;

    @Column(name = "updated_at")
    private ZonedDateTime updatedAt;

    @Column(name="email", nullable = false, unique = true)
    private String email;

    @Column(name="edad", nullable = false)
    private Integer edad;



}
