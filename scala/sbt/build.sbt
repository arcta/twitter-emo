import Dependencies._

lazy val root = (project in file(".")).
    settings(
        inThisBuild(List(
            organization := "me.arcta",
            scalaVersion := "2.11.6",
            version      := "0.1.0-SNAPSHOT"
        )),
        name := "TwitterDataExplorer",
        libraryDependencies ++= Seq(scalaTest % Test,
            "org.apache.spark" %% "spark-core" % "2.2.0" % "provided",
            "org.apache.spark" %% "spark-streaming" % "2.2.0" % "provided",
            "org.apache.bahir" %% "spark-streaming-twitter" % "2.0.1",
            "org.twitter4j" % "twitter4j-core" % "4.0.4",
            "org.twitter4j" % "twitter4j-stream" % "4.0.4"
        )
    )

mergeStrategy in assembly := {
    case PathList("META-INF", xs @ _*) => MergeStrategy.discard
    case x => MergeStrategy.first
}
