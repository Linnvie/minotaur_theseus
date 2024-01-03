package com.linh.apigame.repository;


import com.linh.apigame.Entity.AccountEntity;
import com.linh.apigame.Entity.AccountLevelEntity;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.Optional;

public interface AccountLevelRepository extends JpaRepository<AccountLevelEntity, Long> {
    Page<AccountLevelEntity> findByAccount(Optional<AccountEntity> account, Pageable pageable);

//    @Query(value = "SELECT level_name, mino_start, player_start, size_board, walls, min_moves, moves" +
//            "FROM " +
//            " (SELECT account_level.id as level_id,account_level.moves FROM account INNER JOIN account_level ON account.id = account_level.account_id WHERE account.id = 1) AS subquery" +
//            "INNER JOIN level ON subquery.level_id = level.id",
//
//            countQuery = "SELECT count(*) "+
//            "FROM " +
//            " (SELECT account_level.id as level_id,account_level.moves FROM account INNER JOIN account_level ON account.id = account_level.account_id WHERE account.id = 1) AS subquery" +
//            "INNER JOIN level ON subquery.level_id = level.id")
//    public Page<AccountLevelEntity> findAllByAccountIdAndLevelId(@Param("accountId") long accountId,
//                                                                 Pageable pageable);
}
