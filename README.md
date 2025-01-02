
![telepy](https://github.com/user-attachments/assets/7f859d59-24f3-4144-b9c5-c8378f50cbbe)

<h1 style="text-align:center; color:#4CAF50;">Telegram Number Validator</h1>

<p style="text-align:center; color:#555;">
    This Python application validates Telegram numbers from a CSV file. The app uses the Telethon library to validate phone numbers by checking if they exist in Telegram's database. The results are saved into a CSV file for valid numbers and a text file for invalid numbers. You can also download the CSV of valid numbers and refresh the results from the last uploaded file.
</p>

<h2 style="color:#2196F3;">Features</h2>
<ul>
    <li><b>CSV File Upload:</b> Upload a CSV file containing phone numbers to validate.</li>
    <li><b>Rate-Limited Requests:</b> Ensures API requests are rate-limited to 15 per second to comply with Telegram's rate limits.</li>
    <li><b>Valid Numbers:</b> Extracts and displays valid numbers with usernames or names from Telegram.</li>
    <li><b>Invalid Numbers:</b> Saves invalid numbers along with the reason in a text file.</li>
    <li><b>Download Results:</b> Download the valid numbers in CSV format for further use.</li>
    <li><b>Refresh:</b> Refresh the results by re-uploading the last processed CSV file.</li>
</ul>

<h2 style="color:#2196F3;">Prerequisites</h2>
<p style="color:#555;">Make sure you have the following Python libraries installed:</p>
<ul>
    <li><b>asyncio</b>: For asynchronous programming and handling rate-limited requests.</li>
    <li><b>csv</b>: To read the CSV files containing phone numbers.</li>
    <li><b>threading</b>: For background processing of file uploads and validation.</li>
    <li><b>pandas</b>: For managing and exporting valid numbers into a CSV file.</li>
    <li><b>telethon</b>: For interacting with Telegram's API.</li>
    <li><b>tkinter</b>: For creating the GUI application.</li>
</ul>
<p>Install these libraries using pip:</p>
<pre><code>pip install telethon pandas tkinter</code></pre>

<h2 style="color:#2196F3;">Code Explanation</h2>

<h3 style="color:#4CAF50;">1. Telegram Client Setup</h3>
<p>Set up your Telegram client using your <b>API ID</b> and <b>API Hash</b>.</p>
<pre><code>
api_id = 'your-api-id'
api_hash = 'your-api-key'

client = TelegramClient('session_name', api_id, api_hash)
</code></pre>

<h3 style="color:#4CAF50;">2. File Processing</h3>
<p>The <b>process_file()</b> function allows the user to upload a CSV file containing phone numbers. These numbers are then validated using the <b>rate_limited_get_entity()</b> function to ensure they are within Telegram's rate limit.</p>
<pre><code>
def process_file():
    show_processing_animation()
    threading.Thread(target=process_file_in_background).start()
</code></pre>

<h3 style="color:#4CAF50;">3. Validation</h3>
<p>The <b>validate_numbers()</b> function checks each phone number to determine whether it's valid using Telethon's <b>get_entity()</b> method.</p>
<pre><code>
async def validate_numbers(numbers):
    valid_numbers = []
    invalid_numbers = []
    await client.start()
    for number in numbers:
        user = await rate_limited_get_entity(number)
        if user:
            valid_numbers.append((number, user.username if user.username else user.first_name))
        else:
            invalid_numbers.append((number, "Failed to get entity"))
        await asyncio.sleep(1 / 15)  # Rate-limited to 15 requests/sec
    await client.disconnect()
    return valid_numbers, invalid_numbers
</code></pre>

<h3 style="color:#4CAF50;">4. Exporting Data</h3>
<p>Once validated, valid numbers are saved in a CSV file, and invalid numbers are written to a text file.</p>
<pre><code>
if valid_numbers:
    valid_df = pd.DataFrame(valid_numbers, columns=["Phone Number", "Name"])
    valid_df.to_csv("valid_numbers.csv", index=False)
</code></pre>

<h2 style="color:#2196F3;">GUI Interface</h2>

<p>The app uses <b>tkinter</b> to create a graphical interface. Users can:</p>
<ul>
    <li>Upload a CSV file containing phone numbers</li>
    <li>View valid and invalid numbers</li>
    <li>Download the list of valid numbers in CSV format</li>
    <li>Refresh the list with the last uploaded file</li>
</ul>

<h3 style="color:#4CAF50;">Example Layout</h3>
<table style="border:1px solid #ddd; width:100%; text-align:center;">
    <tr style="background-color:#f2f2f2;">
        <th>Phone Number</th>
        <th>Name</th>
    </tr>
    <tr>
        <td>+919876543210</td>
        <td>John Doe</td>
    </tr>
    <tr>
        <td>+911234567890</td>
        <td>Jane Doe</td>
    </tr>
</table>

<h3 style="color:#4CAF50;">Buttons and Actions</h3>
<ul>
    <li><b>Upload CSV File:</b> Upload a CSV file containing phone numbers for validation.</li>
    <li><b>Refresh:</b> Refresh the results by loading the last uploaded file.</li>
    <li><b>Download CSV:</b> Download the list of valid numbers in CSV format.</li>
</ul>

<h2 style="color:#2196F3;">How to Run</h2>
<ol>
    <li>Set up your Telegram API credentials.</li>
    <li>Run the script:
        <pre><code>python script_name.py</code></pre>
    </li>
    <li>Upload your CSV file to validate phone numbers.</li>
    <li>Download the results or refresh them as needed.</li>
</ol>

<h2 style="color:#2196F3;">Notes</h2>
<ul>
    <li>The script respects Telegram's rate limits (15 requests per second).</li>
    <li>Ensure your CSV file has the phone numbers in the first column.</li>
    <li>If you encounter any issues, check your Telegram API credentials.</li>
</ul>

<p style="text-align:center; color:#555;">
    Enjoy using the Telegram Number Validator! 📱💻
</p>
