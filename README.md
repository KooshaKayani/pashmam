<h1 style='box-sizing: border-box; margin-right: 0px; margin-bottom: 16px; margin-left: 0px; line-height: 1.25; padding-bottom: 0.3em; border-bottom: 1px solid var(--color-border-secondary); caret-color: rgb(36, 41, 46); color: rgb(36, 41, 46); font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif, "Apple Color Emoji", "Segoe UI Emoji"; margin-top: 0px !important;'>pashmam</h1>
<p style='font-size: 16px; box-sizing: border-box; margin-top: 0px; margin-bottom: 16px; caret-color: rgb(36, 41, 46); color: rgb(36, 41, 46); font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif, "Apple Color Emoji", "Segoe UI Emoji";'>Code for team Pashmam (2021 international RCJ) made by Koosha</p>
<p style='font-size: 16px; box-sizing: border-box; margin-top: 0px; margin-bottom: 16px; caret-color: rgb(36, 41, 46); color: rgb(36, 41, 46); font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif, "Apple Color Emoji", "Segoe UI Emoji";'><span style="color: rgb(226, 80, 65);">!! Please read the copyright rule before using the code in any way !!</span></p>
<p style='font-size: 16px; box-sizing: border-box; margin-top: 0px; margin-bottom: 16px; caret-color: rgb(36, 41, 46); color: rgb(36, 41, 46); font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif, "Apple Color Emoji", "Segoe UI Emoji";'><br></p>
<h2 style='font-size: 16px; box-sizing: border-box; margin-top: 0px; caret-color: rgb(36, 41, 46); color: rgb(36, 41, 46); font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif, "Apple Color Emoji", "Segoe UI Emoji"; margin-bottom: 0px !important;'>Attachments:</h2>
<ul>
    <li style='font-size: 16px; box-sizing: border-box; margin-top: 0px; caret-color: rgb(36, 41, 46); color: rgb(36, 41, 46); font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif, "Apple Color Emoji", "Segoe UI Emoji"; margin-bottom: 0px !important;'>Motors:&nbsp;<ul>
            <li style='font-size: 16px; box-sizing: border-box; margin-top: 0px; caret-color: rgb(36, 41, 46); color: rgb(36, 41, 46); font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif, "Apple Color Emoji", "Segoe UI Emoji"; margin-bottom: 0px !important;'>3 large motors.&nbsp;</li>
            <li style='font-size: 16px; box-sizing: border-box; margin-top: 0px; caret-color: rgb(36, 41, 46); color: rgb(36, 41, 46); font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif, "Apple Color Emoji", "Segoe UI Emoji"; margin-bottom: 0px !important;'>1 small motor.&nbsp;</li>
        </ul>
    </li>
    <li style='font-size: 16px; box-sizing: border-box; margin-top: 0px; caret-color: rgb(36, 41, 46); color: rgb(36, 41, 46); font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif, "Apple Color Emoji", "Segoe UI Emoji"; margin-bottom: 0px !important;'>Sensors:&nbsp;<ul>
            <li style='font-size: 16px; box-sizing: border-box; margin-top: 0px; caret-color: rgb(36, 41, 46); color: rgb(36, 41, 46); font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif, "Apple Color Emoji", "Segoe UI Emoji"; margin-bottom: 0px !important;'>2 reflection / color sensor.&nbsp;</li>
            <li style='font-size: 16px; box-sizing: border-box; margin-top: 0px; caret-color: rgb(36, 41, 46); color: rgb(36, 41, 46); font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif, "Apple Color Emoji", "Segoe UI Emoji"; margin-bottom: 0px !important;'>1 infread sensor (ultrasonic works as well).&nbsp;</li>
            <li style='font-size: 16px; box-sizing: border-box; margin-top: 0px; caret-color: rgb(36, 41, 46); color: rgb(36, 41, 46); font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif, "Apple Color Emoji", "Segoe UI Emoji"; margin-bottom: 0px !important;'>1 pixycam2.</li>
        </ul>
    </li>
</ul>
<h2 style='font-size: 16px; box-sizing: border-box; margin-top: 0px; margin-bottom: 16px; caret-color: rgb(36, 41, 46); color: rgb(36, 41, 46); font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif, "Apple Color Emoji", "Segoe UI Emoji";'>Description:</h2>
<h3 style='color: rgb(212, 212, 212); background-color: rgb(30, 30, 30); font-family: Menlo, Monaco, "Courier New", monospace; font-size: 14px; line-height: 21px; white-space: pre;'><span style="color: rgb(220, 220, 170);">Line_follow</span>(<span style="color: rgb(156, 220, 254);">PG</span>, <span style="color: rgb(156, 220, 254);">Speed</span>):</h3>
<p><span style="font-family: Helvetica;">input:</span></p>
<ul>
    <li><span style="font-family: Helvetica;">PG: Proportional Gain. (int)</span></li>
    <li><span style="font-family: Helvetica;">Speed (mm per second) (int)</span></li>
    <li><span style="font-family: Helvetica;">it also reads the value of the color sensors within the function.</span></li>
</ul>
<p><span style="font-family: Helvetica;">output:</span></p>
<ul>
    <li><span style="font-family: Helvetica;">does not return a value.</span></li>
</ul>
<p><span style="font-family: Helvetica;">Use:</span></p>
<ul>
    <li><span style="font-family: Helvetica;">when called in a loop ( in our case the main while loop ) it tracks the main black line using the light reflection of both color sensors.</span></li>
</ul>
<h3 style='color: rgb(212, 212, 212); background-color: rgb(30, 30, 30); font-family: Menlo, Monaco, "Courier New", monospace; font-size: 14px; line-height: 21px; white-space: pre;'><span style="color: rgb(86, 156, 214);">def</span> <span style="color: rgb(220, 220, 170);">obstacles</span>():</h3>
<p><span style="font-family: Helvetica;">input:</span></p>
<ul>
    <li><span style="font-family: Helvetica;">it reads the value of the IR sensors within the function.</span></li>
</ul>
<p><span style="font-family: Helvetica;">output:</span></p>
<ul>
    <li><span style="font-family: Helvetica;">does not return a value.</span></li>
</ul>
<p><span style="font-family: Helvetica;">Use:</span></p>
<ul>
    <li>
        <font face="Helvetica">when called avoids a nearby obstacle detected by ir or ultra sonic sensor by turning around It from the left side.</font>
    </li>
    <li>
        <font face="Helvetica">finds the line by looking for the reflection from the light sensor.</font>
    </li>
</ul>
<p class="Please set custom CSS styles in Settings"><br></p>
<h3 style='color: rgb(212, 212, 212); background-color: rgb(30, 30, 30); font-family: Menlo, Monaco, "Courier New", monospace; font-size: 14px; line-height: 21px; white-space: pre;'><span style="color: rgb(44, 130, 201); background-color: rgb(0, 0, 0);">def</span><span style="background-color: rgb(0, 0, 0);">&nbsp;<span style="color: rgb(247, 218, 100);">green_decision():</span></span></h3>
<p><span style="font-family: Helvetica;">input:</span></p>
<ul>
    <li><span style="font-family: Helvetica;">it reads the value of the color sensors within the function.</span></li>
</ul>
<p><span style="font-family: Helvetica;">output:</span></p>
<ul>
    <li><span style="font-family: Helvetica;">does not return a value.</span></li>
</ul>
<p><span style="font-family: Helvetica;">Use:</span></p>
<ul>
    <li><span style="font-family: Helvetica;">when called evaluates the position of the green block by checking different condition to make the final decision of turning and the direction.</span></li>
    <li>
        <font face="Helvetica">How it functions is much more complicated, please have a look at the code and read the description there in order to understand.</font>
    </li>
</ul>
<h3 style='color: rgb(212, 212, 212); background-color: rgb(30, 30, 30); font-family: Menlo, Monaco, "Courier New", monospace; font-size: 14px; line-height: 21px; white-space: pre;'><span style="color: rgb(86, 156, 214);">def</span> <span style="color: rgb(220, 220, 170);">res_kit</span>():</h3>
<p><span style="font-family: Helvetica;">input:</span></p>
<ul>
    <li><span style="font-family: Helvetica;">No inputs.</span></li>
</ul>
<p><span style="font-family: Helvetica;">output:</span></p>
<ul>
    <li><span style="font-family: Helvetica;">does not return a value.</span></li>
</ul>
<p><span style="font-family: Helvetica;">Use:</span></p>
<ul>
    <li>
        <font face="Helvetica"><span style="font-family: Helvetica;">when called goes through a set of actions:</span></font>
    </li>
    <li><span style="font-family: Helvetica;">moving the sensors out of the way.</span></li>
    <li><span style="font-family: Helvetica;">
            <font face="Helvetica">lowering the arm.&nbsp;</font>
        </span></li>
    <li><span style="font-family: Helvetica;">going forward.</span></li>
    <li><span style="font-family: Helvetica;">using the sensors to push the kit in the arm.</span></li>
    <li><span style="font-family: Helvetica;">and finally lifting the arm.</span></li>
</ul>
<p><br></p>
