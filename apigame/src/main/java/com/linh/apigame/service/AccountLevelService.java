package com.linh.apigame.service;

import com.linh.apigame.dto.PageLevelDto;
import org.springframework.stereotype.Service;

@Service
public interface AccountLevelService {

    PageLevelDto getAllLevelByAccount(int currentPage, int perPage);
}
