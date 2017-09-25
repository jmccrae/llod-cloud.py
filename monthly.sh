#!/bin/bash

die() { echo "$@" 1>&2 ; exit 1; }

NOW=`date +%s`
TDA=$(($NOW - 28 * 24 * 60 * 60))
FDA=$(($NOW - 56 * 24 * 60 * 60))
THIS_MONTH=`date +%b%Y`
THIS_MONTH_NICE=`date "+%B %Y"`
LAST_MONTH=`date --date="@$TDA" +%b%Y`
LAST_MONTH_NICE=`date --date="@$TDA" "+%B %Y"`
PRELAST_MONTH=`date --date="@$FDA" +%b%Y`
PRELAST_MONTH_NICE=`date --date="@$FDA" "+%B %Y"`

#python datahub.py || die
#cp llod-cloud.json ../linguistic-lod/site/llod-cloud-$THIS_MONTH.json
#
#cd ../linguistic-lod/site/
#rm llod-cloud.json
#ln -s llod-cloud-$THIS_MONTH.json llod-cloud.json
#sudo ln -s `pwd`/llod-cloud-$THIS_MONTH.json /var/www/linguistic-lod/html/llod-cloud.json
#
#echo "Please go to http://linguistic-lod.org/llod-cloud and save the diagram as site/images/llod-cloud-$THIS_MONTH.svg to the GitHub repo liderproject/linguistic-lod"
#echo "Press any key when OK"
#read

git pull

rm images/llod-cloud-latest.svg
ln -s images/llod-cloud-$THIS_MONTH.svg images/llod-cloud-latest.svg

cat > llod-cloud-$THIS_MONTH.php << EOF
<?php 
    \$title = "LLOD Cloud ($THIS_MONTH_NICE)";
    include 'header';
?>
   <!-- Page Title
   ================================================== -->
   <div id="page-title">

      <div class="row">

         <div class="ten columns centered text-center">
            <h1>The Linguistic Linked Open Data Cloud<span>.</span></h1>
            <h3>$THIS_MONTH_NICE</h3>

            <p></p>
         </div>

      </div>

   </div> <!-- Page Title End-->

   <!-- Content
   ================================================== -->
   <div class="content-outer">

      <div id="page-content" class="row page">

         <div id="primary" class="twelve columns">

            <section>

                <img src="images/llod-cloud-$THIS_MONTH.svg"/>

            </section> <!-- section end -->
         <div class="four columns">
            <h3><a href="llod-cloud.php">&lt;&lt; Latest</a></h3>
         </div>
         <div class="four columns">
            <h3 style="text-align:right;"><a href="llod-cloud-$LAST_MONTH.php">$LAST_MONTH_NICE &gt;&gt;</a></h3>
         </div>


         </div> <!-- primary end -->

      </div> <!-- page-content End-->

   </div> <!-- Content End-->
<?php include 'footer'; ?>
EOF

cat > llod-cloud-$LAST_MONTH.php << EOF
<?php 
    \$title = "LLOD Cloud ($LAST_MONTH_NICE)";
    include 'header';
?>
   <!-- Page Title
   ================================================== -->
   <div id="page-title">

      <div class="row">

         <div class="ten columns centered text-center">
            <h1>The Linguistic Linked Open Data Cloud<span>.</span></h1>
            <h3>$LAST_MONTH_NICE</h3>

            <p></p>
         </div>

      </div>

   </div> <!-- Page Title End-->

   <!-- Content
   ================================================== -->
   <div class="content-outer">

      <div id="page-content" class="row page">

         <div id="primary" class="twelve columns">

            <section>

                <img src="images/llod-cloud-$LAST_MONTH.svg"/>

            </section> <!-- section end -->
         <div class="four columns">
            <h3><a href="llod-cloud-$THIS_MONTH.php">&lt;&lt; $THIS_MONTH_NICE</a></h3>
         </div>
         <div class="four columns">
            <h3 style="text-align:right;"><a href="llod-cloud-$PRELAST_MONTH.php">$PRELAST_MONTH_NICE &gt;&gt;</a></h3>
         </div>


         </div> <!-- primary end -->

      </div> <!-- page-content End-->

   </div> <!-- Content End-->
<?php include 'footer'; ?>
EOF

mv llod-cloud-versions.html tmp
echo "<li><a href="llod-cloud-$THIS_MONTH.php">$THIS_MONTH_NICE</a></li>" > llod-cloud-versions.html
cat tmp >> llod-cloud-versions.html
rm tmp

git add llod-cloud-$THIS_MONTH.json llod-cloud-$THIS_MONTH.php
git commit -am "LLOD cloud added for $THIS_MONTH_NICE"
git push

sudo cp -r * /var/www/linguistic-lod/html/
