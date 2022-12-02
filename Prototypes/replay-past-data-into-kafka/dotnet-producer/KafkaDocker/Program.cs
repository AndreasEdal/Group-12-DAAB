using Newtonsoft.Json;
using Confluent.Kafka;
using Confluent.SchemaRegistry;
using Confluent.SchemaRegistry.Serdes;
using KafkaDocker;


var config = new ProducerConfig
{
    BootstrapServers = "kafka:9092",
};
/*
string[]  files = {"/App/commitMessage.json", "App/programmingLanguages.json","authorAndCommitMessage.json"};
string[] topics = { "commits", "languages","author" };
for (int i = 0; i < files.Length; i++)
{
    
}
*/
using var producer = new ProducerBuilder<Null, string>(config).Build();
try
{
    using (StreamReader sr = new StreamReader("/App/commitMessage.json"))
    {
        while (!sr.EndOfStream)
        {
            string? json = await sr.ReadLineAsync();
            //Console.WriteLine(json);
            var result = await producer.ProduceAsync("test", new Message<Null, string> { Value = json }); 
            //Console.WriteLine(json);   
        }
    }
}
catch (Exception e)
{
    Console.WriteLine(e.ToString());
}

//return;


var avroSerializerConfig = new AvroSerializerConfig
{
    // optional Avro serializer properties:
    BufferBytes = 100,
};

var schemaRegistryConfig = new SchemaRegistryConfig
{
    // Note: you can specify more than one schema registry url using the
    // schema.registry.url property for redundancy (comma separated list). 
    // The property name is not plural to follow the convention set by
    // the Java implementation.
    Url = "http://schema-registry:8081"
};

using (var schemaRegistry = new CachedSchemaRegistryClient(schemaRegistryConfig))
using (var producer2 =
       new ProducerBuilder<Null, Commit>(config)
           .SetValueSerializer(new AvroSerializer<Commit>(schemaRegistry, avroSerializerConfig))
           .Build())
{
    using (StreamReader sr1 = new StreamReader("/App/commitMessage.json"))
    {
        while (!sr1.EndOfStream)
        {
            var json = await sr1.ReadLineAsync();
            //  Console.WriteLine(avroObject);
            var dynamicObject = JsonConvert.DeserializeObject<Commit>(json);
            Console.WriteLine(dynamicObject.ToString());
            var result = await producer2.ProduceAsync("avro_topic", new Message<Null, Commit> { Value = dynamicObject });
            
        }
    }
}




