#!/bin/bash
#MIT License
#
#Copyright (c) 2018 Kento A. Lauzon
#
#Permission is hereby granted, free of charge, to any person obtaining a copy
#of this software and associated documentation files (the "Software"), to deal
#in the Software without restriction, including without limitation the rights
#to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#copies of the Software, and to permit persons to whom the Software is
#furnished to do so, subject to the following conditions:
#
#The above copyright notice and this permission notice shall be included in all
#copies or substantial portions of the Software.
#
#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#SOFTWARE.


echo "<head>";
echo '<meta charset="utf-8">';
echo '<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0-beta.3/css/bootstrap.min.css" integrity="sha384-Zug+QiDoJOrZ5t4lssLdxGhVrurbmBWopoEl+M6BdEfwnCJZtKxi1KgxUyJq13dy" crossorigin="anonymous">';
echo "</head>";

cd ${1};

TEAM_NAME=$(basename $(git remote show -n origin | grep Fetch | cut -d: -f2-));
BRANCH=$(git -C . rev-parse --abbrev-ref HEAD);
echo "<div id=${TEAM_NAME}>";
echo "<h1>";
echo "${TEAM_NAME}";
echo "</h1>";
echo "";
echo "<p>branch : $BRANCH</p>";

git log --format='%aN' | sort -u > contributors.txt

SHORTLOG=$(git shortlog -sn --no-merges);

echo "<table class='table'>";
echo "<thead class='thead-dark'>";
echo "<th>Author</th><th>Commit count</th><th>Lines Added</th><th>Lines Deleted</th><th>Total (delta)</th><th>Ratio A/D (%)</th>";
echo "<th><abbr title='Contributors with less than 10% are highlighted in red.'>
Team Percentage <sup>(?)</sup>
</div></th>";
echo "</thead><tbody>";

# Calculate total lines added by all members, for the whole repository $GRAND_TOTAL
declare $(git log --numstat --no-merges -w --pretty=tformat: *.java | gawk '{loc += $1 - $2; } END { printf "GRAND_TOTAL=%s", loc }' -)

while read author; do
    printf "<tr name='${TEAM_NAME}_${author}'>";

    LOG=$(git log --no-merges --author="${author}" --pretty=tformat: --numstat -w *.java | gawk '{ add += $1; subs += $2; loc += $1 - $2; } END { printf "ADD=%s\nSUB=%s\nTOTAL=%s", add, subs, loc }' -)
    declare $LOG;
    
    COMMIT_COUNT=$(echo "$SHORTLOG" | grep -m 1 "${author}" | gawk '{print $1}');
    TEAM_PERCENTAGE=$((100*TOTAL/(GRAND_TOTAL + 1)));
    STYLE=""
    if [ "$TEAM_PERCENTAGE" -le "10" ]; then
	STYLE="style='background-color:#F07979; font-weight:bold;'";
    fi
    printf "<td $STYLE>";
    printf "${author}";
    printf "</td>";
    printf "<td name='commit-count' $STYLE>${COMMIT_COUNT}</td>";
    printf "<td name='add' $STYLE>${ADD}</td>";
    printf "<td name='sub' $STYLE>${SUB}</td>";
    printf "<td name='total' $STYLE>${TOTAL}</td>";
    printf "<td name='ratio' $STYLE>$((100*ADD/(SUB + 1)))</td>";
    printf "<td name='team-percentage' $STYLE>${TEAM_PERCENTAGE}</td>";
    
    printf "</tr>";
done <contributors.txt
echo "</tbody></table>";

echo "</div>";
