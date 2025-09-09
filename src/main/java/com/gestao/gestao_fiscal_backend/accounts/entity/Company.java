package com.gestao.gestao_fiscal_backend.accounts.entity;

import jakarta.persistence.*;

@Entity
@Table(name="companies")
public class Company {
  @Id
  @GeneratedValue(strategy = GenerationType.AUTO)
  @Column(nullable = false)
  private Long id;

  @Column(nullable = false)
  private String name;

  @Column(name="isActive")
  private Boolean isActive;

}
