package com.example.photoviewer;

import java.util.HashSet;
import java.util.List;
import java.util.Set;

// 앱 전역에서 게시물 목록을 공유하기 위한 Singleton 클래스
public class DataHolder {
    private static DataHolder instance;
    private List<Post> postList;
    private Set<String> previousImageUrls = new HashSet<>(); // 이전 동기화의 이미지 URL 저장
    private Set<String> newImageUrls = new HashSet<>(); // 새로 추가된 이미지 URL

    private DataHolder() {} // 외부에서 생성 방지

    public static synchronized DataHolder getInstance() {
        if (instance == null) {
            instance = new DataHolder();
        }
        return instance;
    }

    public void setPostList(List<Post> postList) {
        this.postList = postList;
    }

    public List<Post> getPostList() {
        return postList;
    }

    // 이전 이미지 URL 저장
    public void setPreviousImageUrls(Set<String> urls) {
        this.previousImageUrls = urls;
    }

    public Set<String> getPreviousImageUrls() {
        return previousImageUrls;
    }

    // 새로운 이미지 URL 저장
    public void setNewImageUrls(Set<String> urls) {
        this.newImageUrls = urls;
    }

    public Set<String> getNewImageUrls() {
        return newImageUrls;
    }
}