val scala3Version = "2.12.0"

lazy val root = project
  .in(file("."))
  .settings(
    name := "hello-world",
    version := "0.1.0-SNAPSHOT",

    scalaVersion := scala3Version,

    libraryDependencies += "org.apache.spark" %% "spark-sql" % "3.3.0"

  )
