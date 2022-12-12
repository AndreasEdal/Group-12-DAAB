using Avro;
using Avro.Specific;

namespace KafkaDocker;

public class Commit : ISpecificRecord


{
    public static Schema _SCHEMA = Avro.Schema.Parse(@"{""type"": ""record"",""name"": ""Commit"",""namespace"": ""ca.dataedu"",""fields"": [{""name"": ""parent"",""type"": {""type"": ""array"",""items"": ""string""}},{""name"": ""tree"",""type"": ""string""},{""name"": ""commit"",""type"": ""string""},{ ""name"": ""author"",""type"": {""name"": ""author"",""type"": ""record"",""fields"": [{""name"": ""name"",""type"": ""string""},{""name"": ""email"",""type"": ""string""},{""name"": ""time_sec"",""type"": ""string""},{""name"": ""tz_offset"",""type"": ""string""},{""name"": ""date"",""type"": ""string""}]}},{""name"": ""committer"",""type"": {""name"": ""committer"",""type"": ""record"",""fields"": [{""name"": ""name"",""type"": ""string""},{""name"": ""email"",""type"": ""string""},{""name"": ""time_sec"",""type"": ""string""},{""name"": ""tz_offset"",""type"": ""string""},{""name"": ""date"",""type"": ""string""}]}},{""name"": ""subject"",""type"": ""string""},{""name"": ""message"",""type"": ""string""},{""name"": ""repo_name"",""type"": ""string""}]");
    public string parent;
    public string tree;
    public string commit;
    public  Array author; 
    public string author_name; 
    public string author_email;
    public string author_time_sec;
    public string author_tz_offset;
    public string author_date;
    public Array commiter;
    public string commiter_name;
    public string commiter_email;
    public string commiter_time_sec;
    public string commiter_tz_offset;
    public string commiter_date;
    public string subject;
    public string message;
    public string repo_name;
    public virtual Schema Schema => _SCHEMA;

    public object Get(int fieldPos)
    {
        switch (fieldPos)
        {
            case 0: return this.parent;
            case 1: return this.tree;
            case 2: return this.commit;
            case 3: return this.author;
            case 4: return this.author_name;
            case 5: return this.author_email;
            case 6: return this.author_time_sec;
            case 7: return this.author_tz_offset;
            case 8: return this.author_date;
            case 9: return this.commiter;
            case 10: return this.commiter_name;
            case 11: return this.commiter_email;
            case 12: return this.commiter_time_sec;
            case 13: return this.commiter_tz_offset;
            case 14: return this.commiter_date;
            case 15: return this.subject;
            case 16: return this.message;
            case 17: return this.repo_name;
            
            default: throw new AvroRuntimeException("Bad index " + fieldPos + " in Get()");
        };
    }

    public void Put(int fieldPos, object fieldValue)
    {
        switch (fieldPos)
        {
            case 0: this.parent = (System.String)fieldValue; break;
            case 1:  this.tree = (System.String)fieldValue; break;
            case 2:  this.commit = (System.String)fieldValue; break;
            case 3:  this.author = (System.Array)fieldValue; break;
                // create array 
            case 4:  this.author_name = (System.String)fieldValue; 
                this.author.Add(string, this.author_name);
                break;
                // add to index 0
            case 5:  this.author_email = (System.String)fieldValue; break;
                // add to index 1
            case 6:  this.author_time_sec = (System.String)fieldValue; break;
            case 7:  this.author_tz_offset = (System.String)fieldValue; break;
            case 8:  this.author_date = (System.String)fieldValue; break;
            case 9:  this.commiter = (System.Array)fieldValue; break;
            case 10:  this.commiter_name = (System.String)fieldValue; break;
            case 11:  this.commiter_email = (System.String)fieldValue; break;
            case 12:  this.commiter_time_sec = (System.String)fieldValue; break;
            case 13:  this.commiter_tz_offset = (System.String)fieldValue; break;
            case 14:  this.commiter_date = (System.String)fieldValue; break;
            case 15:  this.subject = (System.String)fieldValue; break;
            case 16:  this.message = (System.String)fieldValue; break;
            case 17:  this.repo_name = (System.String)fieldValue; break; 
            default: throw new AvroRuntimeException("Bad index " + fieldPos + " in Put()");
        };
    }
    public override string ToString()
    {
        return $"Commit: {this.commit}, msg:'{this.message.Trim()}'";
    }
    
}