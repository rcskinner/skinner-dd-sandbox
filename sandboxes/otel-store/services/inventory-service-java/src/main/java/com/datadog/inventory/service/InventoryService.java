package com.datadog.inventory.service;

import com.datadog.inventory.model.InventoryItem;
import org.springframework.stereotype.Service;

import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import java.util.concurrent.ConcurrentHashMap;

@Service
public class InventoryService {
    private final Map<String, InventoryItem> inventory = new ConcurrentHashMap<>();

    public List<InventoryItem> getAllItems() {
        return new ArrayList<>(inventory.values());
    }

    public InventoryItem getItem(String id) {
        InventoryItem item = inventory.get(id);
        if (item == null) {
            throw new RuntimeException("Item not found");
        }
        return item;
    }

    public InventoryItem createItem(InventoryItem item) {
        if (inventory.containsKey(item.getId())) {
            throw new RuntimeException("Item already exists");
        }
        inventory.put(item.getId(), item);
        return item;
    }

    public InventoryItem updateItem(String id, InventoryItem item) {
        if (!inventory.containsKey(id)) {
            throw new RuntimeException("Item not found");
        }
        item.setId(id);
        inventory.put(id, item);
        return item;
    }

    public void deleteItem(String id) {
        if (!inventory.containsKey(id)) {
            throw new RuntimeException("Item not found");
        }
        inventory.remove(id);
    }

    public InventoryItem updateQuantity(String id, int quantity) {
        InventoryItem item = getItem(id);
        item.setQuantity(quantity);
        return updateItem(id, item);
    }
} 