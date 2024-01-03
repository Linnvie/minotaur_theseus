package com.linh.apigame.dto;

public class PageableDto {
    private int totalPages;

    private long totalElements;

    private int perPage;

    private int numberOfElements;

    private int currentPage;

    private boolean first;

    private boolean last;

    public PageableDto(int totalPages, long totalElements, int perPage,
                       int numberOfElements, int currentPage,
                       boolean first, boolean last) {
        this.totalPages = totalPages;
        this.totalElements = totalElements;
        this.perPage = perPage;
        this.numberOfElements = numberOfElements;
        this.currentPage = currentPage;
        this.first = first;
        this.last = last;
    }

    public PageableDto() {
    }

    public int getTotalPages() {
        return totalPages;
    }

    public void setTotalPages(int totalPages) {
        this.totalPages = totalPages;
    }

    public long getTotalElements() {
        return totalElements;
    }

    public void setTotalElements(long totalElements) {
        this.totalElements = totalElements;
    }

    public int getPerPage() {
        return perPage;
    }

    public void setPerPage(int perPage) {
        this.perPage = perPage;
    }

    public int getNumberOfElements() {
        return numberOfElements;
    }

    public void setNumberOfElements(int numberOfElements) {
        this.numberOfElements = numberOfElements;
    }

    public int getCurrentPage() {
        return currentPage;
    }

    public void setCurrentPage(int currentPage) {
        this.currentPage = currentPage;
    }

    public boolean isFirst() {
        return first;
    }

    public void setFirst(boolean first) {
        this.first = first;
    }

    public boolean isLast() {
        return last;
    }

    public void setLast(boolean last) {
        this.last = last;
    }
}
