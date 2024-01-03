package com.linh.apigame.controller;

import com.linh.apigame.Entity.AccountLevelEntity;
import com.linh.apigame.Entity.LevelEntity;
import com.linh.apigame.dto.PageLevelDto;
import com.linh.apigame.service.LevelService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.awt.*;
import java.util.List;

@RestController
@RequestMapping("/api/v1")
public class LevelController {

    @Autowired
    private LevelService levelService;

    @GetMapping(path="/level")
    @ResponseBody
    public ResponseEntity<?> getPaginateLevel(
            @RequestParam(value = "currentPage", defaultValue = "1") int currentPage,
            @RequestParam(value = "perPage", defaultValue = "10") int perPage){

        PageLevelDto list = levelService.getAllLevel(currentPage-1,perPage);

        return ResponseEntity.ok().body(list);
    }

    @GetMapping(path="/level1")
    @ResponseBody
    public List<AccountLevelEntity> getPaginateLeve(
            @RequestParam(value = "currentPage", defaultValue = "1") int currentPage,
            @RequestParam(value = "perPage", defaultValue = "10") int perPage){
List<AccountLevelEntity> a = levelService.all(currentPage-1,perPage);
       ;

//        return ResponseEntity.ok().body(a);
        return a;
    }
}
