package com.linh.apigame.Entity;

import jakarta.persistence.*;

import java.util.ArrayList;
import java.util.List;


@Entity
@Table(name="level")
public class LevelEntity {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(name="level_name", length=20)
    private String levelName;

    @Column(name="size_board", length=20)
    private String sizeBoard;

    @Column(name="mino_start", length=20)
    private String minoStart;

    @Column(name="player_start", length=20)
    private String playerStart;

    @Column(name="goal", length=20)
    private String goal;

    @Column(name="walls", columnDefinition = "TEXT")
    private String walls;

    @Column(name="min_moves")
    private int minMoves;


    @OneToMany(mappedBy="level")
    private List<AccountLevelEntity> listAccountLevel = new ArrayList<>();

    public Long getId() {
        return id;
    }

    public void setId(Long id) {
        this.id = id;
    }

    public String getLevelName() {
        return levelName;
    }

    public void setLevelName(String levelName) {
        this.levelName = levelName;
    }

    public String getSizeBoard() {
        return sizeBoard;
    }

    public void setSizeBoard(String sizeBoard) {
        this.sizeBoard = sizeBoard;
    }

    public String getMinoStart() {
        return minoStart;
    }

    public void setMinoStart(String minoStart) {
        this.minoStart = minoStart;
    }

    public String getPlayerStart() {
        return playerStart;
    }

    public void setPlayerStart(String playerStart) {
        this.playerStart = playerStart;
    }

    public String getGoal() {
        return goal;
    }

    public void setGoal(String goal) {
        this.goal = goal;
    }

    public String getWalls() {
        return walls;
    }

    public void setWalls(String walls) {
        this.walls = walls;
    }

    public int getMinMoves() {
        return minMoves;
    }

    public void setMinMoves(int minMoves) {
        this.minMoves = minMoves;
    }

    public List<AccountLevelEntity> getListAccountLevel() {
        return listAccountLevel;
    }

    public void setListAccountLevel(List<AccountLevelEntity> listAccountLevel) {
        this.listAccountLevel = listAccountLevel;
    }
}
