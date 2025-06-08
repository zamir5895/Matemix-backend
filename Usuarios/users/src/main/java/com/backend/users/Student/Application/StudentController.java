package com.backend.users.Student.Application;

import com.backend.users.Student.DTOs.RequestDTO;
import com.backend.users.Student.Domain.StudentService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api/students")
public class StudentController {
    @Autowired
    private StudentService studentService;
    @PostMapping("/profile")
    public ResponseEntity<?> getStudentProfile(@RequestBody RequestDTO dto) {
        try {
            return ResponseEntity.ok(studentService.getStudentProfile(dto));
        } catch (Exception e) {
            return ResponseEntity.status(500).body("Error: " + e.getMessage());
        }
    }






}
