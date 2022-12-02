using Newtonsoft.Json;
using Confluent.Kafka;
using Confluent.SchemaRegistry;
using Confluent.SchemaRegistry.Serdes;
using KafkaDocker;
using SolTechnology.Avro;


var config = new ProducerConfig
{
    BootstrapServers = "kafka:9092",
};
using var producer = new ProducerBuilder<Null, string>(config).Build();
try
{
    using (StreamReader sr = new StreamReader("/App/commitMessage.json"))
    {
        while (!sr.EndOfStream)
        {
            string? json = await sr.ReadLineAsync();
            //Console.WriteLine(json);
            var result = await producer.ProduceAsync("commits_json", new Message<Null, string> { Value = json }); 
            //Console.WriteLine(json);   
        }
    }
}
catch (Exception e)
{
    Console.WriteLine(e.ToString());
}

return;


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
            
            Commit dynamicObject = JsonConvert.DeserializeObject<Commit>(json);
            dynamicObject.commit.Trim();
            dynamicObject.message.Trim();
            Console.WriteLine(dynamicObject);
            byte[] avroObject = AvroConvert.Serialize(dynamicObject, CodecType.Snappy);
            //Commit deserializedObject = AvroConvert.Deserialize(byte[] avroObject, typeof(Commit));
            var str = System.Text.Encoding.ASCII.GetString(avroObject);
            //Console.WriteLine(str);
            var result = await producer2.ProduceAsync("commits_avro", new Message<Null, Commit> { Value = dynamicObject ?? new Commit() });
            //var result = await producer2.ProduceAsync("avro_topic2", new Message<Null, byte[]> { Value = avroObject });
            
        }
    }
}




