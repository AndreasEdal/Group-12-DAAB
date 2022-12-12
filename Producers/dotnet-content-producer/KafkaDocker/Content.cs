namespace KafkaDocker;
using Avro;
using Avro.Specific;

public class Content : ISpecificRecord
{
    public static Schema _SCHEMA = Avro.Schema.Parse(@"{""name"": ""Content"",""type"": ""record"", ""namespace"": ""com.acme.avro"",""fields"": [{""name"": ""id"", ""type"": ""string""},{""name"": ""size"",""type"": ""string""},{""name"": ""content"",""type"": ""string"" },{""name"": ""binary"",""type"": ""boolean""},{""name"": ""copies"", ""type"": ""string""},{""name"": ""sample_repo_name"",""type"": ""string""},{""name"": ""sample_ref"",""type"": ""string""},{""name"": ""sample_path"",""type"": ""string""},{""name"": ""sample_mode"",""type"": ""string""}]}");

    public string id;
    public string size;
    public string content;
    public bool binary;
    public string samples_repo_name;
    public string sample_ref;
    public string sample_path;
    public string sample_mode;
    public virtual Schema Schema => _SCHEMA;

    
    public void Put(int fieldPos, object fieldValue)
    {
        switch (fieldPos)
        {
            case 0: this.id = (System.String)fieldValue;
                break; 
            case 1: this.size = (System.String)fieldValue;
                break; 
            case 2: this.content = (System.String)fieldValue;
                break; 
            case 3: this.binary = (System.Boolean)fieldValue;
                break; 
            case 4: this.samples_repo_name = (System.String)fieldValue;
                break; 
            case 5: this.sample_ref = (System.String)fieldValue;
                break; 
            case 6: this.sample_path = (System.String)fieldValue;
                break; 
            case 7: this.sample_mode = (System.String)fieldValue;
                break; ;
            default: throw new AvroRuntimeException("Bad index " + fieldPos + " in Get()");
        }

       
    }
    public object Get(int fieldPos)
    {
        switch (fieldPos)
        {
            case 0: return this.id;
            case 1: return this.size;
            case 2: return this.content;
            case 3: return this.binary;
            case 4: return this.samples_repo_name;
            case 5: return this.sample_ref;
            case 6: return this.sample_path;
            case 7: return this.sample_mode;
            default: throw new AvroRuntimeException("Bad index " + fieldPos + " in Get()");


        }
    }
}