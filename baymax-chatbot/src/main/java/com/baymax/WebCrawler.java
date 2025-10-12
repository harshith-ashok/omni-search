package com.baymax;

import org.jsoup.Jsoup;
import org.jsoup.nodes.Document;
import org.jsoup.nodes.Element;
import org.jsoup.select.Elements;

import java.io.IOException;
import java.net.MalformedURLException;
import java.net.URL;
import java.util.*;

public class WebCrawler {
    private int maxPages;
    private Set<String> visited;

    public WebCrawler(int maxPages) {
        this.maxPages = maxPages;
        this.visited = new HashSet<>();
    }

    public List<Map<String, String>> crawl(String startUrl, String keyword) {
        List<Map<String, String>> results = new ArrayList<>();
        Queue<String> queue = new LinkedList<>();
        queue.add(startUrl);

        while (!queue.isEmpty() && visited.size() < maxPages) {
            String url = queue.poll();
            if (visited.contains(url)) {
                continue;
            }

            try {
                Document doc = Jsoup.connect(url)
                        .userAgent("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")
                        .timeout(5000)
                        .get();

                visited.add(url);

                String title = doc.title();
                if (title.isEmpty()) {
                    title = "No Title";
                }

                String text = doc.text();
                String[] words = text.split("\\s+");
                String snippet = String.join(" ", 
                    Arrays.copyOf(words, Math.min(50, words.length)));

                if (keyword == null || 
                    keyword.toLowerCase().contains(text.toLowerCase()) ||
                    keyword.toLowerCase().contains(title.toLowerCase())) {
                    
                    Map<String, String> item = new LinkedHashMap<>();
                    item.put("url", url);
                    item.put("title", title);
                    item.put("snippet", snippet);
                    results.add(item);
                }

                Elements links = doc.select("a[href]");
                for (Element link : links) {
                    String href = link.attr("href");
                    String fullUrl = new URL(new URL(url), href).toString();
                    if (isValidUrl(fullUrl)) {
                        queue.add(fullUrl);
                    }
                }

            } catch (Exception e) {
                continue;
            }
        }

        return results;
    }

    private boolean isValidUrl(String urlString) {
        try {
            URL url = new URL(urlString);
            return url.getHost() != null && !url.getHost().isEmpty() &&
                   url.getProtocol() != null && !url.getProtocol().isEmpty();
        } catch (MalformedURLException e) {
            return false;
        }
    }
}
