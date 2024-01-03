package com.linh.apigame.Entity;

import jakarta.persistence.*;

@Entity
@Table(name="account_level")
public class AccountLevelEntity {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @ManyToOne(fetch= FetchType.LAZY)
    @JoinColumn(name="account_id")
    private AccountEntity account;

    @ManyToOne(fetch= FetchType.LAZY)
    @JoinColumn(name="level_id")
    private LevelEntity level;

    @Column(name="moves")
    private int moves;

    public Long getId() {
        return id;
    }

    public void setId(Long id) {
        this.id = id;
    }

    public AccountEntity getAccount() {
        return account;
    }

    public void setAccount(AccountEntity account) {
        this.account = account;
    }

    public LevelEntity getLevel() {
        return level;
    }

    public void setLevel(LevelEntity level) {
        this.level = level;
    }

    public int getMoves() {
        return moves;
    }

    public void setMoves(int moves) {
        this.moves = moves;
    }
}
