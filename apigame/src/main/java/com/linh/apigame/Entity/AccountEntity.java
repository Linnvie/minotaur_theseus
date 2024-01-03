package com.linh.apigame.Entity;

import jakarta.persistence.*;

import java.util.ArrayList;
import java.util.List;

@Entity
@Table(name="account")
public class AccountEntity {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(name="account_name", length=20, unique = true)
    private String accountName;

    @Column(name="password", length=20)
    private String password;

    @OneToMany(mappedBy="account")
    private List<AccountLevelEntity> listAccountLevel = new ArrayList<>();

    public Long getId() {
        return id;
    }

    public void setId(Long id) {
        this.id = id;
    }

    public String getAccountName() {
        return accountName;
    }

    public void setAccountName(String accountName) {
        this.accountName = accountName;
    }

    public List<AccountLevelEntity> getListAccountLevel() {
        return listAccountLevel;
    }

    public void setListAccountLevel(List<AccountLevelEntity> listAccountLevel) {
        this.listAccountLevel = listAccountLevel;
    }

    public String getPassword() {
        return password;
    }

    public void setPassword(String password) {
        this.password = password;
    }
}
