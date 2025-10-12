package com.baymax;

import org.jsoup.Jsoup;
import org.jsoup.nodes.Document;
import org.jsoup.nodes.Element;
import org.jsoup.select.Elements;

import java.io.IOException;
import java.util.*;

public class DuckDuckGoSearch {
    private static final String BASE_URL = "https://html.duckduckgo.com/html/";

    public List<Map<String, String>> search(String query, int numResults) {
        List<Map<String, String>> results = new ArrayList<>();

        try {
            Document doc = Jsoup.connect(BASE_URL)
                    .userAgent("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
                    .data("q", query)
                    .timeout(5000)
                    .post();

            Elements links = doc.select("a.result__a");
            int count = 0;

            for (Element link : links) {
                if (count >= numResults) break;

                String title = link.text();
                String url = link.attr("href");
                Element snippetTag = link.closest("div.result").selectFirst("a.result__snippet");
                String snippet = snippetTag != null ? snippetTag.text() : "";

                Map<String, String> item = new LinkedHashMap<>();
                item.put("title", title);
                item.put("url", url);
                item.put("snippet", snippet);
                results.add(item);
                count++;
            }

        } catch (IOException e) {
            e.printStackTrace();
        }

        return results;
    }
}