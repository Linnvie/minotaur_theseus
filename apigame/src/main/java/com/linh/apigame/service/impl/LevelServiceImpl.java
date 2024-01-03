package com.linh.apigame.service.impl;

import com.linh.apigame.Entity.AccountEntity;
import com.linh.apigame.Entity.AccountLevelEntity;
import com.linh.apigame.Entity.LevelEntity;
import com.linh.apigame.dto.LevelDto;
import com.linh.apigame.dto.PageLevelDto;
import com.linh.apigame.repository.AccountLevelRepository;
import com.linh.apigame.repository.AccountRepository;
import com.linh.apigame.repository.LevelRepository;
import com.linh.apigame.service.LevelService;
import org.modelmapper.ModelMapper;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.PageRequest;
import org.springframework.data.domain.Pageable;
import org.springframework.data.domain.Sort;
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.Optional;
import java.util.stream.Collectors;

@Service
public class LevelServiceImpl implements LevelService {

    @Autowired
    private LevelRepository levelRepository;

    @Autowired
    private AccountLevelRepository repository;

    @Autowired
    private AccountRepository acrepository;

    @Autowired
    private ModelMapper modelMapper;


    @Override
    public PageLevelDto getAllLevel(int currentPage, int perPage) {

        Pageable paging = PageRequest.of(currentPage, perPage);
        Page<LevelEntity> pageListEntity
                = this.levelRepository.findAllByAccountIdAndLevelId(1,paging);
        return pageListEntity.getTotalElements() > 0
                ?  new PageLevelDto(pageListEntity.getTotalPages(),
                pageListEntity.getTotalElements(),
                pageListEntity.getSize(),
                pageListEntity.getNumberOfElements(),
                pageListEntity.getNumber() + 1,
                pageListEntity.isFirst(),
                pageListEntity.isLast(),
                pageListEntity.getContent().stream()
                        .map(item -> modelMapper.map(item, LevelDto.class))
                        .collect(Collectors.toList()))
                : null;

    }

    @Override
    public List<AccountLevelEntity> all(int currentPage, int perPage) {
        Optional<AccountEntity> account = acrepository.findById(Long.valueOf(1));
        Pageable paging = PageRequest.of(currentPage, perPage);
//        Page<AccountLevelEntity> pageListEntity
//                = this.repository.findAllByAccount(account);
        return account.get().getListAccountLevel();
    }
}
