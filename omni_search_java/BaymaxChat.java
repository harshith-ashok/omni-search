package com.baymax;

import com.google.gson.*;
import org.apache.hc.client5.http.classic.HttpClient;
import org.apache.hc.client5.http.classic.methods.HttpPost;
import org.apache.hc.client5.http.impl.classic.HttpClients;
import org.apache.hc.core5.http.HttpEntity;
import org.apache.hc.core5.http.io.entity.StringEntity;

import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.util.*;

public class BaymaxChat {
    private String model;
    private String host;
    private Map<String, List<Map<String, String>>> sessions;
    private Gson gson;
    private String systemPrompt;

    public BaymaxChat() {
        this.model = "llama3.2";
        this.host = "http://localhost:11434";
        this.sessions = new HashMap<>();
        this.gson = new Gson();
        this.systemPrompt = "SYSTEM PROMPT – "UNIFIED TRUSTED SUMMARIZER\n\n" +
            "You are a factual summarizer that generates concise, reliable summaries of user search queries using information strictly from trusted public knowledge sources such as Wikipedia, Britannica, official government or institutional websites (e.g., .gov, .edu, .org).\n\n" +
            "Your output will be used as the system prompt for a locally running AI model, so it must be:\n" +
            "- Factually correct\n" +
            "- Neutral and objective\n" +
            "- Simple and clear in language\n" +
            "- Free of speculation, opinion, or bias\n" +
            "- Free of formatting errors or unnecessary markup\n" +
            "- Free of personal data, unverified claims, or unsafe content\n\n" +
            "You must always perform the following steps:\n\n" +
            "1. **Interpretation:**\n" +
            "   - Identify the key topic or question the user wants summarized.\n\n" +
            "2. **Trusted Source Constraint:**\n" +
            "   - Use or simulate information *only* from trusted knowledge bases such as Wikipedia, Britannica, or verified institutional repositories.\n\n" +
            "3. **Summarization:**\n" +
            "   - Present a concise, factual summary in 8-9 sentences.\n" +
            "   - Maintain chronological, logical, or definitional structure depending on context.\n" +
            "   - Do not include hyperlinks or citations, but assume the information was derived from verified sources.\n\n" +
            "4. **Output Format:**\n" +
            "   As a plain text without formatting\n\n" +
            "Your tone should always remain:\n" +
            "- Neutral\n" +
            "- Informative\n" +
            "- Compact\n" +
            "- Readable by both humans and machines";
    }

    public String chat(String userMessage, String sessionId) {
        if (!sessions.containsKey(sessionId)) {
            List<Map<String, String>> history = new ArrayList<>();
            Map<String, String> systemMsg = new LinkedHashMap<>();
            systemMsg.put("role", "system");
            systemMsg.put("content", systemPrompt);
            history.add(systemMsg);
            sessions.put(sessionId, history);
        }

        List<Map<String, String>> history = sessions.get(sessionId);
        Map<String, String> userMsg = new LinkedHashMap<>();
        userMsg.put("role", "user");
        userMsg.put("content", userMessage);
        history.add(userMsg);

        try {
            Map<String, Object> payload = new LinkedHashMap<>();
            payload.put("model", model);
            payload.put("messages", history);
            payload.put("stream", false);

            HttpClient client = HttpClients.createDefault();
            HttpPost httpPost = new HttpPost(host + "/api/chat");
            httpPost.setEntity(new StringEntity(gson.toJson(payload)));
            httpPost.setHeader("Content-type", "application/json");

            String reply = client.execute(httpPost, response -> {
                if (response.getCode() == 200) {
                    BufferedReader reader = new BufferedReader(
                        new InputStreamReader(response.getEntity().getContent()));
                    StringBuilder result = new StringBuilder();
                    String line;
                    while ((line = reader.readLine()) != null) {
                        result.append(line);
                    }
                    JsonObject jsonObj = JsonParser.parseString(result.toString())
                        .getAsJsonObject();
                    return jsonObj.getAsJsonObject("message")
                        .get("content").getAsString();
                } else {
                    return "Error: " + response.getCode();
                }
            });

            Map<String, String> assistantMsg = new LinkedHashMap<>();
            assistantMsg.put("role", "assistant");
            assistantMsg.put("content", reply);
            history.add(assistantMsg);

            return reply;

        } catch (Exception e) {
            return "Error: " + e.getMessage();
        }
    }
}