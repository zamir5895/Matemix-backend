package com.backend.users.Security.Auth.Service;


import com.backend.users.Profesor.Domain.Professor;
import com.backend.users.Profesor.Infrastructure.ProfessorRepository;
import com.backend.users.Salon.Domain.Salon;
import com.backend.users.Salon.Infrastructure.SalonRepository;
import com.backend.users.Security.Auth.DTOs.*;
import com.backend.users.Student.Domain.Student;
import com.backend.users.Student.Infrastructure.StudentRepository;
import com.backend.users.User.Domain.Rol;
import com.backend.users.User.Domain.User;
import com.backend.users.User.Infrastructure.UserRepository;
import com.opencsv.CSVWriter;
import jakarta.persistence.EntityNotFoundException;
import org.springframework.beans.factory.annotation.Qualifier;
import org.springframework.core.io.ByteArrayResource;
import org.springframework.http.RequestEntity;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Service;
import org.springframework.web.multipart.MultipartFile;
import com.opencsv.CSVReader;

import java.io.ByteArrayOutputStream;
import java.io.InputStreamReader;
import java.io.OutputStreamWriter;
import java.time.ZonedDateTime;
import java.util.*;

@Service
public class AuthService {

    private final StudentRepository studentRepository;
    private final PasswordEncoder passwordEncoder;
    private final ProfessorRepository professorRepository;
    private final UserRepository userRepository;
    private final SalonRepository salonRepository;


    public AuthService(StudentRepository studentRepository, PasswordEncoder passwordEncoder, ProfessorRepository professorRepository, @Qualifier("userRepository") UserRepository userRepository,  SalonRepository salonRepository) {
        this.studentRepository = studentRepository;
        this.passwordEncoder = passwordEncoder;
        this.professorRepository = professorRepository;
        this.userRepository = userRepository;
        this.salonRepository = salonRepository;
    }

    public ByteArrayResource processRegisterForStuedents(MultipartFile file, Long professorId) throws Exception {
        List<String[]> result = new ArrayList<>();
        result.add(new String[]{"Nombre", "Apellido", "Usename", "Contraseña", "DNI", "Grado", "Seccion", "Status", "Message"});
        try (CSVReader reader = new CSVReader(new InputStreamReader(file.getInputStream()))) {
            String[] line;
            reader.readNext(); // Saltar la cabecera del archivo CSV
            Optional<Professor> optionalProfessor = professorRepository.findById(professorId);
            if (optionalProfessor.isEmpty()) {
                throw new RuntimeException("El profesor no existe");
            }
            List<Salon> salones = salonRepository.findByProfesorId(professorId);
            if (salones.isEmpty()) {
                throw new RuntimeException("El profesor no tiene salones");
            }

            Map<String, Salon> salonCache = new HashMap<>();

            while ((line = reader.readNext()) != null) {
                String grado = line[3].trim();
                String seccion = line[4].trim();
                String salonKey = grado + "-" + seccion;

                Salon salon = salonCache.computeIfAbsent(salonKey, key ->
                        salones.stream()
                                .filter(s -> s.getGrado().equals(grado) && s.getSeccion().equals(seccion))
                                .findFirst()
                                .orElseThrow(() -> new RuntimeException("El salon no existe"))
                );

                if (salon.getProfesor().getId() != professorId) {
                    throw new RuntimeException("El profesor no tiene acceso a este salon");
                }

                String nombre = line[0].trim();
                String apellido = line[1].trim();
                String dni = line[2].trim();

                if (studentRepository.existsStudentByDni(Long.valueOf(dni))) {
                    result.add(new String[]{nombre, apellido, generateUsername(nombre, apellido, seccion), dni, dni, grado, seccion, "Error", "El DNI ya existe, no puede repetirse los dnis"});
                    continue;
                }

                String userName = generateUsername(nombre, apellido, dni);
                String password = passwordEncoder.encode(dni);
                Student student = new Student();
                student.setDni(Long.valueOf(dni));
                student.setSalon(salon);
                student.setEmail(userName);
                student.setFirstName(nombre);
                student.setLastName(apellido);
                student.setRole(Rol.STUDENT);
                student.setPassword(password);
                student.setCreatedAt(ZonedDateTime.now());
                studentRepository.save(student);
                result.add(new String[]{nombre, apellido, userName, password, dni, grado, seccion, "Success", "El usuario se ha creado correctamente"});
            }
        }

        ByteArrayOutputStream b = new ByteArrayOutputStream();
        try (CSVWriter writer = new CSVWriter(new OutputStreamWriter(b))) {
            writer.writeAll(result);
        }
        return new ByteArrayResource(b.toByteArray());
    }
    public void registerProfessor(DtoRegister professor){
        Optional<Professor> optionalProfessor = professorRepository.findByEmail(professor.getCorreo());
        if(optionalProfessor.isPresent()){
            throw new RuntimeException("El profesor ya existe");
        }
        try{
            String password = passwordEncoder.encode(professor.getContraseña());
            Professor professorSave = new Professor();
            professorSave.setCreatedAt(ZonedDateTime.now());
            professorSave.setEmail(professor.getCorreo());
            professorSave.setUpdatedAt(ZonedDateTime.now());
            professorSave.setRole(Rol.TEACHER);
            professorSave.setFirstName(professor.getNombre());
            professorSave.setLastName(professor.getApellido());
            professorSave.setPassword(password);
            professorSave.setCreatedAt(ZonedDateTime.now());
            professorSave.setUpdatedAt(ZonedDateTime.now());
            professorSave.setEdad(professor.getEdad());
            professorRepository.save(professorSave);
        }catch (Exception e){
            throw new RuntimeException("El profesor no se pudo registrar " +e.getMessage());
        }
    }

    public void registerAdmin(DtoRegister register){
        Optional<User> optionalAdmin = userRepository.findByEmail(register.getCorreo());
        if(optionalAdmin.isPresent()){
            throw new RuntimeException("El admin ya existe");
        }
        String password = passwordEncoder.encode(register.getContraseña());
        User adminSave = new Professor();
        adminSave.setCreatedAt(ZonedDateTime.now());
        adminSave.setEmail(register.getCorreo());
        adminSave.setUpdatedAt(ZonedDateTime.now());
        adminSave.setRole(Rol.ADMIN);
        adminSave.setFirstName(register.getNombre());
        adminSave.setLastName(register.getApellido());
        adminSave.setPassword(password);
        adminSave.setCreatedAt(ZonedDateTime.now());
        adminSave.setUpdatedAt(ZonedDateTime.now());
        adminSave.setEdad(register.getEdad());
        userRepository.save(adminSave);
    }

    public AuthDTO login(LoginRequest request){
        Optional<User> optionalUser = userRepository.findByEmail(request.getEmail());
        if(optionalUser.isEmpty()){
            throw new RuntimeException("El usuario no existe");
        }
        User user = optionalUser.get();
        if(!passwordEncoder.matches(request.getPassword(), user.getPassword())){
            throw new RuntimeException("La contraseña es incorrecta");
        }
        AuthDTO login = new AuthDTO();
        login.setId(user.getId().toString());
        login.setUsername(user.getEmail());
        login.setRole(user.getRole().toString());





        return login;
    }

    public void changePassword(DTOChangePassword dto){
        Optional<User> optionalUser = userRepository.findByEmail(dto.getUsername());
        if(optionalUser.isEmpty()){
            throw new RuntimeException("El usuario no existe");
        }
        User user = optionalUser.get();
        String passwordEncode = passwordEncoder.encode(dto.getNewPassword());
        user.setPassword(passwordEncode);
        userRepository.save(user);
    }



    public String generateUsername(String name, String apellido, String dni){
        return name+apellido+dni.substring(0,3);
    }


}
