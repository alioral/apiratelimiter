<h1>Rate Limiter - Sliding Window</h1>

<h2>Introduction</h2>
<p>In order to limit API calls, this sliding window technique is implemented. So methodology is we check for users current request time and compare it with
the earliest request time. After comparing we decide whether there is an opening for the incoming request.</p>

<h2>Questions I've Answered Myself</h2>
<ul>
    <li><p><b>Q:</b>So assume that I've made request and filled up my API request call list. After waiting for hours, do you clear it?</p>
    <p><b>A:</b>No! We compare it with the earliest request you made and then remove the first element and append the current time you made the request. You do not need to worry about clearing your request list. If it's been hours, every request filling up the list will be removed since each of them will be compared to your current size. So instead of thinking "having enough room" as having a clear list, think it as the items that'll be removed, on demand</p></li>
    <li><p><b>Q: </b>Why your test names are like "test_1, test_2" instead of more relevant names like "test_request_first", "test_request_after_rate_limit"?</p>
    <li><p><b>A: </b>Great Question! I'm using Python's incredibly simple unittest module, which is really cool but executes the tests by lexographic order (names) and that's why I wanted to make sure they were working in correct order.</p></li>
</ul>

<h2>Comments</h2>
<p>Overall it was a fun challenge.</p>
