package com.linh.apigame.dto;

import jakarta.persistence.Column;

public class LevelDto {

    private String levelName;

    private String sizeBoard;

    private String minoStart;

    private String playerStart;

    private String goal;

    private String walls;

    private int moves;

    private int minMoves;

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

    public int getMoves() {
        return moves;
    }

    public void setMoves(int moves) {
        this.moves = moves;
    }

    public int getMinMoves() {
        return minMoves;
    }

    public void setMinMoves(int minMoves) {
        this.minMoves = minMoves;
    }
}
