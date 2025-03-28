package com.datadog.inventory.model;

import lombok.Data;
import lombok.Builder;
import lombok.NoArgsConstructor;
import lombok.AllArgsConstructor;

@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class InventoryItem {
    private String id;
    private String name;
    private String description;
    private int quantity;
    private double price;
    private String category;
} 