package com.linh.apigame.service;


import com.linh.apigame.Entity.AccountLevelEntity;
import com.linh.apigame.dto.PageLevelDto;
import org.springframework.data.domain.Page;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
public interface LevelService {
    PageLevelDto getAllLevel(int currentPage, int perPage);

    List<AccountLevelEntity> all(int currentPage, int perPage);
}
