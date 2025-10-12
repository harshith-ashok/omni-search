package com.baymax.controllers;

import com.baymax.*;
import com.baymax.models.ChatRequest;
import org.springframework.web.bind.annotation.*;

import java.io.File;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.*;

@RestController
@CrossOrigin(origins = "*")
public class BaymaxController {

    private static final List<String> FOLDERS = Arrays.asList(
        "Desktop", "Downloads", "Documents", "Pictures", "Movies", "Music"
    );
    private static final String HOME = System.getProperty("user.home");

    private final BaymaxChat baymax;
    private final DuckDuckGoSearch gsearch;
    private final Indexer indexer;

    public BaymaxController() {
        this.baymax = new BaymaxChat();
        this.gsearch = new DuckDuckGoSearch();
        this.indexer = new Indexer("index.json");
    }

    @GetMapping("/local")
    public Map<String, Object> searchLocal(@RequestParam String query) {
        List<Map<String, String>> results = new ArrayList<>();
        for (String folder : FOLDERS) {
            String folderPath = HOME + File.separator + folder;
            File dir = new File(folderPath);
            if (!dir.isDirectory()) {
                continue;
            }
            File[] files = dir.listFiles();
            if (files != null) {
                for (File file : files) {
                    if (!file.getName().startsWith(".") && 
                        file.getName().toLowerCase().contains(query.toLowerCase())) {
                        Map<String, String> item = new LinkedHashMap<>();
                        item.put("folder", folder);
                        item.put("file", file.getName());
                        results.add(item);
                    }
                }
            }
        }
        Map<String, Object> response = new LinkedHashMap<>();
        response.put("results", results);
        return response;
    }

    @GetMapping("/local-deep")
    public Map<String, Object> searchDeep(@RequestParam String query) {
        List<Map<String, String>> results = new ArrayList<>();
        for (String folder : FOLDERS) {
            String folderPath = HOME + File.separator + folder;
            File dir = new File(folderPath);
            if (!dir.isDirectory()) {
                continue;
            }
            searchDirectory(dir, folderPath, folder, query, results, 0);
        }
        Map<String, Object> response = new LinkedHashMap<>();
        response.put("results", results);
        return response;
    }

    private void searchDirectory(File dir, String basePath, String folder, 
                                 String query, List<Map<String, String>> results, int depth) {
        if (depth > 4) {
            return;
        }

        File[] files = dir.listFiles();
        if (files != null) {
            for (File file : files) {
                if (file.isDirectory()) {
                    searchDirectory(file, basePath, folder, query, results, depth + 1);
                } else if (!file.getName().startsWith(".") && 
                           file.getName().toLowerCase().contains(query.toLowerCase())) {
                    Map<String, String> item = new LinkedHashMap<>();
                    item.put("folder", folder);
                    String subfolder = file.getParent().replace(basePath, "");
                    if (subfolder.startsWith(File.separator)) {
                        subfolder = subfolder.substring(1);
                    }
                    item.put("subfolder", subfolder.isEmpty() ? "" : subfolder);
                    item.put("file", file.getName());
                    results.add(item);
                }
            }
        }
    }

    @PostMapping("/chat")
    public Map<String, String> chat(@RequestBody ChatRequest request) {
        String reply = baymax.chat(request.getMessage(), request.getSession_id());
        Map<String, String> response = new LinkedHashMap<>();
        response.put("reply", reply);
        return response;
    }

    @PostMapping("/index")
    public Map<String, Object> indexSite(
            @RequestParam String start_url,
            @RequestParam(defaultValue = "5") int max_pages) {
        List<Map<String, String>> data = indexer.buildIndex(start_url, max_pages);
        Map<String, Object> response = new LinkedHashMap<>();
        response.put("indexed", data.size());
        response.put("data", data);
        return response;
    }

    @GetMapping("/search")
    public Map<String, Object> searchIndex(@RequestParam String query) {
        List<Map<String, String>> results = indexer.searchIndex(query);
        Map<String, Object> response = new LinkedHashMap<>();
        response.put("query", query);
        response.put("results", results);
        return response;
    }

    @GetMapping("/gquery")
    public Map<String, Object> googleQuery(
            @RequestParam String query,
            @RequestParam(defaultValue = "5") int num_results) {
        List<Map<String, String>> results = gsearch.search(query, num_results);
        Map<String, Object> response = new LinkedHashMap<>();
        response.put("query", query);
        response.put("results", results);
        return response;
    }
}
