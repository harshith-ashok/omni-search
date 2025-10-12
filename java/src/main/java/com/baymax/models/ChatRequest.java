package com.baymax.models;

public class ChatRequest {
    private String message;
    private String session_id = "default";

    public ChatRequest() {}

    public ChatRequest(String message, String session_id) {
        this.message = message;
        this.session_id = session_id;
    }

    public String getMessage() {
        return message;
    }

    public void setMessage(String message) {
        this.message = message;
    }

    public String getSession_id() {
        return session_id;
    }

    public void setSession_id(String session_id) {
        this.session_id = session_id;
    }
}
