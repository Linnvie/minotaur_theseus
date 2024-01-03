package com.linh.apigame.dto;

import java.util.List;

public class PageLevelDto extends PageableDto{

    private List<LevelDto> listLevel;

    public PageLevelDto(int totalPages, long totalElements, int perPage, int numberOfElements, int currentPage, boolean first, boolean last, List<LevelDto> listLevel) {
        super(totalPages, totalElements, perPage, numberOfElements, currentPage, first, last);
        this.listLevel = listLevel;
    }

    public PageLevelDto() {
    }

    public List<LevelDto> getListLevel() {
        return listLevel;
    }

    public void setListLevel(List<LevelDto> listLevel) {
        this.listLevel = listLevel;
    }
}
