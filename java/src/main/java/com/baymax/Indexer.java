package com.baymax;

import com.google.gson.Gson;
import com.google.gson.GsonBuilder;
import com.google.gson.reflect.TypeToken;

import java.io.*;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.*;

public class Indexer {
    private String indexFile;
    private Gson gson;

    public Indexer(String indexFile) {
        this.indexFile = indexFile;
        this.gson = new GsonBuilder().setPrettyPrinting().create();
    }

    public List<Map<String, String>> buildIndex(String startUrl, int maxPages) {
        WebCrawler crawler = new WebCrawler(maxPages);
        List<Map<String, String>> data = crawler.crawl(startUrl, null);

        List<Map<String, String>> existingData = new ArrayList<>();
        try {
            String content = new String(Files.readAllBytes(Paths.get(indexFile)));
            existingData = gson.fromJson(content, 
                new TypeToken<List<Map<String, String>>>(){}.getType());
            if (existingData == null) {
                existingData = new ArrayList<>();
            }
        } catch (IOException e) {
            existingData = new ArrayList<>();
        }

        existingData.addAll(data);

        try (FileWriter writer = new FileWriter(indexFile)) {
            gson.toJson(existingData, writer);
        } catch (IOException e) {
            e.printStackTrace();
        }

        return data;
    }

    public List<Map<String, String>> searchIndex(String keyword) {
        List<Map<String, String>> results = new ArrayList<>();
        try {
            String content = new String(Files.readAllBytes(Paths.get(indexFile)));
            List<Map<String, String>> data = gson.fromJson(content,
                new TypeToken<List<Map<String, String>>>(){}.getType());
            if (data == null) {
                return results;
            }

            for (Map<String, String> entry : data) {
                String title = entry.getOrDefault("title", "").toLowerCase();
                String snippet = entry.getOrDefault("snippet", "").toLowerCase();
                if (title.contains(keyword.toLowerCase()) || 
                    snippet.contains(keyword.toLowerCase())) {
                    results.add(entry);
                }
            }

        } catch (IOException e) {
            return results;
        }

        return results;
    }
}