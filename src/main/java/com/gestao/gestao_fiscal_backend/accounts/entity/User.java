package com.gestao.gestao_fiscal_backend.accounts.entity;

import jakarta.persistence.*;
import jakarta.validation.constraints.Email;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.Size;
import lombok.Getter;
import lombok.Setter;

import java.time.LocalDateTime;

@Getter
@Setter
@Entity
@Table(name="users")
public class User {
  @Id
  @GeneratedValue(strategy = GenerationType.AUTO)
  @Column(nullable = false)
  private Long id;

  @NotBlank
  @Email
  @Column(nullable = false)
  private String email;

  @NotBlank
  @Column(nullable = false)
  private String password;

  @ManyToOne
  @JoinColumn(name = "companyId")
  private Company companyActive;

  @Size(max = 50)
  @Column(name = "firstName", length = 50)
  private String firstName;

  @Size(max = 50)
  @Column(name = "lastName", length = 50)
  private String lastName;

  @Column(name = "firstAccess")
  private Boolean firstAccess;

  @Column(name = "lastLogin")
  private LocalDateTime lastLogin;

  @Column(name = "createdAt")
  private LocalDateTime createdAt;

  @Column(name = "updatedAt")
  private LocalDateTime updatedAt;

  public Company getCompanyActive() {
    return companyActive;
  }

  public void setCompanyActive(Company companyActive) {
    this.companyActive = companyActive;
  }

}
