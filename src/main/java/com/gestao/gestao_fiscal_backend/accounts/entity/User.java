package com.gestao.gestao_fiscal_backend.accounts.entity;

import jakarta.persistence.*;
import jakarta.validation.constraints.Email;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.Size;

import java.time.LocalDateTime;

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
  @JoinColumn(name = "company_id")
  private Company company_active;

  @Size(max = 50)
  @Column(name = "first_name", length = 50)
  private String firstName;

  @Size(max = 50)
  @Column(name = "last_name", length = 50)
  private String lastName;

  @Column(name = "first_access")
  private Boolean firstAccess;

  @Column(name = "last_login")
  private LocalDateTime lastLogin;

  @Column(name = "created_at")
  private LocalDateTime createdAt;

  @Column(name = "updated_at")
  private LocalDateTime updatedAt;

  public Company getCompany_active() {
    return company_active;
  }

  public void setCompany_active(Company company_active) {
    this.company_active = company_active;
  }

}
