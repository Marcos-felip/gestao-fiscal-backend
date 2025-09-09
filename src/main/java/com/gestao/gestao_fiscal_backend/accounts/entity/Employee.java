package com.gestao.gestao_fiscal_backend.accounts.entity;
import com.gestao.gestao_fiscal_backend.accounts.enuns.EmployeeRole;
import jakarta.persistence.*;
import jakarta.validation.constraints.NotBlank;

@Entity
@Table(name="employees")
public class Employee {
    @Id
    @GeneratedValue(strategy = GenerationType.AUTO)
    @Column(nullable = false)
    private Long id;

    @Column(nullable = false)
    @NotBlank
    private String name;

    @OneToOne
    @JoinColumn(name = "userId", referencedColumnName = "id", nullable = false)
    private User user;

    @ManyToOne
    @JoinColumn(name = "companyId")
    private Company company;

    @Column(name="isActive")
    private Boolean isActive;

    @Enumerated(EnumType.STRING)
    @Column(name="role", nullable = false)
    private EmployeeRole role;
}
