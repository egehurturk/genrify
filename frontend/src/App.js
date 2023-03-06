import { Fragment, useState } from 'react'
// function classNames(...classes) {
//   return classes.filter(Boolean).join(' ')
// }

function getExtension(filename) {
  return filename.split('.').pop()
}

function checkFile(file) {
  return getExtension(file.name).toLowerCase() === "mp3" && 
         file.size <= 10000000
}

export default function Example() {

  const [youtubeLink, setYoutubeLink]   = useState("")
  const [youtubeLinkUploaded, setYoutubeLinkUploaded] =  useState(false)
  const [fileUploaded, setFileUploaded] =  useState(false)
  const [file, setFile] = useState();

  


  const handleSubmit = (event) => {
    event.preventDefault();
    const data = new FormData(event.target);

    fetch('http://127.0.0.1:8000/api/demo', {
      method: 'POST',
      body: data
    })
    .then( res => console.log(res))
    .catch(error => console.log(error))
  }

  const handleFileUpload = (event) => {
    if (event.target.files) {
      checkFile(event.target.files[0])
       
      if (checkFile(event.target.files[0])) {
          console.log("saving...")
          setFile(event.target.files[0]);
          setFileUploaded(true);

      }
      else {
        alert(`${event.target.files[0].name} is not a mp3 file. Only mp3 files are accepted for upload`)
      }
    } else {
      alert("No files are uploaded")
    }
  }

  const handleInputChange = (event) => {
    setYoutubeLink(event.target.value);
    setYoutubeLinkUploaded(true);

    // make the file upload disable

    
  }

  return (
    <>
      <div className="min-h-full">

        <div className="bg-gray-800 pb-32">
          <header className="py-10">
            <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
              <h1 className="text-6xl text-center font-bold tracking-tight text-white">Genrify</h1>
            </div>
          </header>
        </div>

        {/* MAIN CONTENT */}
        <main className="-mt-32">
          <div className="mx-auto max-w-5xl px-4 pb-12 sm:px-6 lg:px-8">
            <form onSubmit={handleSubmit} method="post" className="space-y-8" encType='multipart/form-data'>
              <div className="space-y-8">

                {/* FORM BLOCK */}
                <div className="pt-8">
                  <div className="grid grid-cols-1 gap-y-6 gap-x-4 sm:grid-cols-6">
                    <div className="sm:col-span-6 flex rounded-md shadow-sm">
                      <div className="mt-4 relative flex flex-grow items-stretch focus-within:z-10">
                        <input
                          type="text"
                          name="song-link-text"
                          id="song-link-text"
                          disabled={fileUploaded}
                          autoComplete="text"
                          onChange={handleInputChange}
                          placeholder='Enter YouTube link'
                          className="block w-full bg-gray-700 rounded-lg text-gray-300 shadow-sm placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-300 sm:text-sm sm:leading-6 disabled:bg-gray-800 disabled:cursor-not-allowed disabled:text-white disabled:border-dashed disabled:border-2 disabled:ring-gray-200"
                        />
                      </div>
                     
                    </div>
                  </div>
                </div>

                {/* OR  */}
                <div className='flex items-center justify-center'>
                    <div className="mt-4 mb-2 w-1/12 bg-gray-500 rounded-xl">
                      <h3 className='text-center text-white'>OR</h3>
                    </div>
                </div>

                {/* UPLOAD BLOCK */}
                <div className="mt-6 grid grid-cols-1 gap-y-6 gap-x-4 sm:grid-cols-6">
                  <div className="sm:col-span-6">
                    <div className=" mt-2 flex justify-center rounded-md border-2 border-dashed border-gray-300 px-6 pt-5 pb-6">
                      <div className="space-y-1 text-center">
                        <svg
                          className="mx-auto h-12 w-12 text-gray-400"
                          stroke="currentColor"
                          fill="none"
                          viewBox="0 0 48 48"
                          aria-hidden="true"
                        >
                          <path
                            d="M28 8H12a4 4 0 00-4 4v20m32-12v8m0 0v8a4 4 0 01-4 4H12a4 4 0 01-4-4v-4m32-4l-3.172-3.172a4 4 0 00-5.656 0L28 28M8 32l9.172-9.172a4 4 0 015.656 0L28 28m0 0l4 4m4-24h8m-4-4v8m-12 4h.02"
                            strokeWidth={2}
                            strokeLinecap="round"
                            strokeLinejoin="round"
                          />
                        </svg>
                        <div className="flex text-sm text-gray-600">
                          <label
                            htmlFor="file-upload"
                            className="relative cursor-pointer rounded-md font-medium text-indigo-400 focus-within:outline-none focus-within:ring-2 focus-within:ring-indigo-500 focus-within:ring-offset-2 hover:text-indigo-500"
                          >
                            <span>Upload a file</span>
                            <input
                              id="file-upload"
                              name="file-upload"
                              onChange={handleFileUpload}
                              disabled={youtubeLinkUploaded}
                              type="file" 
                              // TODO: CHANGE HERE
                              className="sr-only" />
                          </label>
                          <p className="pl-1">or drag and drop</p>
                          {/* <p className="text-gray-200 pl-1">{file && `${file.name} - ${file.type} - ${file.size}`}</p> */}
                        </div>
                          <p className="text-gray-200 text-sm">{file && `${file.name} - ${file.type} - ${file.size}`} </p>
                          <p className="text-xs text-gray-500">MP3 up to 10MB</p>
                            
                      </div>
                    </div>
                  </div>
                </div>

                {/* SUBMIT button */}
                <div>
                  <button
                    type="submit"
                    className="flex w-full justify-center rounded-md bg-indigo-600 py-2 px-3 text-sm font-semibold text-white shadow-sm hover:bg-indigo-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600"
                  >
                    Search
                  </button>
                </div>

              </div>
            </form>
          </div>
        </main>
      </div>
    </>
  )
}




