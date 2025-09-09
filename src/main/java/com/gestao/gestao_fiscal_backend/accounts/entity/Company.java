package com.gestao.gestao_fiscal_backend.accounts.entity;

import jakarta.persistence.*;

import java.util.List;

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

  @OneToMany(mappedBy = "company", fetch = FetchType.LAZY)
  private List<Employee> employees;

  public List<Employee> getEmployees() {
    return employees;
  }

}
