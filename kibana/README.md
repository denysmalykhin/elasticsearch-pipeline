## How to Create a Dashboard and Visualize Data with Kibana

### Step 1: Upload Data to Elasticsearch
1. Ensure your Elasticsearch instance is running.
2. Use the Kibana Dev Tools or any other method to upload your data to an Elasticsearch index. For example, you can use the following command in Kibana Dev Tools to upload a JSON file:
   ```json
   POST /your_index/_bulk
   { "index" : { "_index" : "your_index", "_id" : "1" } }
   { "field1" : "value1", "field2" : "value2", "date" : "2024-01-01T00:00:00Z" }
   ```

### Step 2: Create a Visualization
1. Navigate to the **Dashboards** section in Kibana.
2. Press **Create visualization** button.
3. Click on Dropdown menu from the left upper corner and select **Create a data view**.
4. Input name for dataview, the index pattern you created earlier (e.g., `metadata_index`) and timestamp field (e.g., `timestamp`).
5. In the **Available fields** dropdown menu select **timestamp** field.

### Step 3: Configure the visualization
1. In the right side menu select any pre-configured visualization type.
2. On the right bottom corner set desired time range for the visualization.
3. After you finished with the configuration, press **Save and return** button.
4. Add few more visualizations to the dashboard and press **Save** button.