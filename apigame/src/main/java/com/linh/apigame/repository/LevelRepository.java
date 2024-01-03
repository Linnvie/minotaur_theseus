package com.linh.apigame.repository;

import com.linh.apigame.Entity.AccountLevelEntity;
import com.linh.apigame.Entity.LevelEntity;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;

public interface LevelRepository extends JpaRepository<LevelEntity, Long> {

    @Query(value = "SELECT level.id, level_name, mino_start, player_start, size_board, goal,walls,min_moves " +
            "FROM " +
            " (SELECT account_level.id as level_id,account_level.moves " +
            "FROM account INNER JOIN account_level " +
            "ON account.id = account_level.account_id WHERE account.id = 1) AS subquery" +
            " INNER JOIN level ON   level.id= subquery.level_id ORDER BY level_name ASC"

            , nativeQuery = true)
    public Page<LevelEntity> findAllByAccountIdAndLevelId(@Param("accountId") long accountId,
                                                                 Pageable pageable);
}
