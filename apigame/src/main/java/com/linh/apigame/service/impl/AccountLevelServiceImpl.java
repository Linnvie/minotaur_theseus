//package com.linh.apigame.service.impl;
//
//import com.linh.apigame.Entity.AccountLevelEntity;
//import com.linh.apigame.dto.LevelDto;
//import com.linh.apigame.dto.PageLevelDto;
//import com.linh.apigame.repository.AccountLevelRepository;
//import com.linh.apigame.service.AccountLevelService;
//import org.springframework.beans.factory.annotation.Autowired;
//import org.springframework.data.domain.Page;
//import org.springframework.data.domain.PageRequest;
//import org.springframework.data.domain.Pageable;
//import org.springframework.data.domain.Sort;
//import org.springframework.stereotype.Service;
//
//@Service
//public class AccountLevelServiceImpl implements AccountLevelService {
//
//    @Autowired
//    private AccountLevelRepository accountLevelRepository;
//    @Override
//    public PageLevelDto getAllLevelByAccount(int currentPage, int perPage) {
//        Pageable paging = PageRequest.of(currentPage, perPage, Sort.by("levelName").ascending());
//        Page<AccountLevelEntity> pageListEntity
//                = this.accountLevelRepository.findAll(paging);
////        return pageListEntity.getTotalElements() > 0
////                ?  new PageLevelDto(pageListEntity.getTotalPages(),
////                pageListEntity.getTotalElements(),
////                pageListEntity.getSize(),
////                pageListEntity.getNumberOfElements(),
////                pageListEntity.getNumber() + 1,
////                pageListEntity.isFirst(),
////                pageListEntity.isLast(),
////                pageListEntity.getContent().stream()
////                        .map(item -> modelMapper.map(item, LevelDto.class))
////                        .collect(Collectors.toList()))
////                : null;
//        return null;
//    }
//}
